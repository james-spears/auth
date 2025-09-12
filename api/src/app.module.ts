import { Module } from '@nestjs/common';
import { ConfigModule } from '@nestjs/config';
import { AppController } from './app.controller';
import { AppService } from './app.service';
import { CacheService } from './cache/cache.service';

@Module({
  imports: [
    ConfigModule.forRoot({
      expandVariables: true,
      isGlobal: true,
    }),
  ],
  controllers: [AppController],
  providers: [AppService, CacheService],
})
export class AppModule {}
