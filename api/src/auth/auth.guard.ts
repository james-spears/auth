import {
  CanActivate,
  ExecutionContext,
  Injectable,
  Logger,
} from '@nestjs/common';
import { Request } from 'express';
import crypto from 'node:crypto';
import { ConfigService } from '@nestjs/config';
import { CacheService } from '../cache/cache.service';

function validateSignature(
  message: string,
  signature: string,
  salt: string,
  secretKey: string,
): [boolean, string] {
  // Create an HMAC object with the SHA256 algorithm and the secret key.
  console.log(salt + secretKey);
  const hmac = crypto.createHmac('sha256', salt + secretKey);
  // Update the HMAC with the message data.
  // console.log(s)
  hmac.update(message);

  // Calculate the HMAC digest (signature) and return it in hexadecimal format.
  const calculatedSignature = hmac.digest('base64url');
  const receivedHmacBuffer = Buffer.from(signature, 'base64url');
  const calculatedHmacBuffer = Buffer.from(calculatedSignature, 'base64url');
  const isValid = crypto.timingSafeEqual(
    receivedHmacBuffer,
    calculatedHmacBuffer,
  );
  return [isValid, calculatedSignature];
}

@Injectable()
export class AuthGuard implements CanActivate {
  private readonly logger = new Logger(AuthGuard.name);
  constructor(
    private configService: ConfigService,
    private cacheService: CacheService,
  ) {}

  async canActivate(context: ExecutionContext): Promise<boolean> {
    const request = context.switchToHttp().getRequest<Request>();
    const secretKey = this.configService.get<string>('SECRET_KEY');
    const salt = this.configService.get<string>('SALT') || '';
    this.logger.verbose(`secretKey: ${secretKey}`);
    if (typeof secretKey === 'undefined') {
      this.logger.error('secret key is not set');
      return false;
    }
    const xAuthorizationKey = request.headers['x-authorization-key'];
    this.logger.verbose(`xAuthorizationKey: ${xAuthorizationKey}`);
    if (typeof xAuthorizationKey === 'undefined') {
      this.logger.error('authorization key is undefined');
      return false;
    }
    if (Array.isArray(xAuthorizationKey)) {
      this.logger.error('multiple authorization keys found');
      return false;
    }
    const signedMessage = await this.cacheService.client.get(
      `:1:${xAuthorizationKey}` as string,
    );
    this.logger.verbose(`signedMessage: ${signedMessage}`);
    if (!signedMessage) {
      this.logger.error('signed message not in cache');
      return false;
    }
    const parts: string[] = JSON.parse(signedMessage).split(':');
    if (parts.length !== 2) {
      this.logger.error('message format is invalid');
      return false;
    }
    const [message, signature] = parts;
    const [isValid, calculatedSignature] = validateSignature(
      message,
      signature,
      salt,
      secretKey,
    );
    this.logger.verbose(`calculatedSignature: ${calculatedSignature}`);
    if (!isValid) {
      this.logger.error('unable to validate signature');
      return false;
    }
    // Create a Buffer object from the Base64 string, specifying 'base64' as the encoding
    const buffer = Buffer.from(message, 'base64url');

    // Convert the Buffer to a string using the desired encoding (e.g., 'utf8')
    const decodedMessage = buffer.toString('utf8');
    this.logger.verbose(`decodedMessage: ${decodedMessage}`);
    try {
      const user = JSON.parse(decodedMessage);
      request.user = user;
      return true;
    } catch (e) {
      if (e instanceof Error) {
        this.logger.error(e.message);
      }
      return false;
    }
  }
}
