import { HttpParams } from '@angular/common/http';

export class HttpParamsBuilder implements IHttpParamsBuilder {
  private params: HttpParams;

  constructor() {
    this.params = new HttpParams();
  }

  append(param: string, value: any): this {
    if (value) {
      this.params = this.params.append(param, value);
    }
    return this;
  }

  build(): HttpParams {
    return this.params;
  }
}

interface IHttpParamsBuilder {
  append(key: string, value: any): this;
  build(): HttpParams;
}