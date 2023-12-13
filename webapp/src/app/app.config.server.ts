import { provideHttpClient, withFetch, withInterceptors } from '@angular/common/http';
import { mergeApplicationConfig, ApplicationConfig } from '@angular/core';
import { provideServerRendering } from '@angular/platform-server';
import { provideToastr, ToastrModule } from 'ngx-toastr';
import { appConfig } from './app.config';
import { jwtAuthInterceptor } from './interceptors/jwt-auth.interceptor';

const serverConfig: ApplicationConfig = {
  providers: [
    provideServerRendering(),
    provideHttpClient(
      withFetch(),
      // withInterceptors([jwtAuthInterceptor])
    ),     
    provideToastr({
      timeOut: 10000,
      positionClass: 'toast-bottom-right',
      preventDuplicates: true,
    })
  ]
};

export const config = mergeApplicationConfig(appConfig, serverConfig);
