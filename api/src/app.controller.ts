import { Controller, Get, Logger, Req, UseGuards } from '@nestjs/common';
import * as appService from './app.service';
import { AuthGuard } from './auth/auth.guard';
import type { Request } from 'express';

@Controller()
export class AppController {
  private logger: Logger = new Logger(AppController.name);
  constructor(private readonly appService: appService.AppService) {}

  @Get('status')
  getStatus(): appService.Status {
    return this.appService.getStatus();
  }

  @Get('protected')
  @UseGuards(AuthGuard)
  getProtected(@Req() request: Request): appService.Status {
    return this.appService.getProtected();
  }
}
