import { Injectable } from '@nestjs/common';

export type Status = { ok: true };

@Injectable()
export class AppService {
  getStatus(): Status {
    return { ok: true };
  }

  getProtected(): Status {
    return { ok: true };
  }
}
