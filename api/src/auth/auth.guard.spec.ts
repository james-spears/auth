import { ConfigService } from '@nestjs/config';
import { AuthGuard } from './auth.guard';
import { CacheService } from 'src/cache/cache.service';

describe('AuthGuard', () => {
  it('should be defined', () => {
    expect(
      new AuthGuard({} as ConfigService, {} as CacheService),
    ).toBeDefined();
  });
});
