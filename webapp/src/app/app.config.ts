import { ApplicationConfig } from '@angular/core';
import { provideRouter } from '@angular/router';
import { routes } from './app.routes';
import { provideClientHydration } from '@angular/platform-browser';
import { provideHttpClient, withFetch, withInterceptors } from '@angular/common/http';
import { provideToastr, ToastrModule } from 'ngx-toastr';
import { jwtAuthInterceptor } from './interceptors/jwt-auth.interceptor';
import { MatDialog, MatDialogModule } from '@angular/material/dialog';

export const appConfig: ApplicationConfig = {
  providers: [
    provideRouter(routes), 
    provideClientHydration(),
    provideHttpClient(
      withFetch(),
      // withInterceptors([jwtAuthInterceptor])
    ),
    provideToastr({
      timeOut: 7500,
      positionClass: 'toast-bottom-right',
      preventDuplicates: true,
    }),
    MatDialogModule
  ]
};
