import { Injectable } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import Redis from 'ioredis';

@Injectable()
export class CacheService {
  client: Redis;

  constructor(private configService: ConfigService) {
    const nodeEnv = this.configService.get<string>('NODE_ENV');
    if (nodeEnv === 'produciton') {
      this.client = new Redis({
        port: 6379, // Redis port
        host: 'cache', // Redis host
        db: 1, // Defaults to 0
      });
    }
  }
}
