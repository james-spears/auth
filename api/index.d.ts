// src/types/express.d.ts
import { Request } from 'express';

declare module 'express' {
  interface Request {
    user?: any; // TODO - type this
  }
}
