import { bootstrapApplication, provideProtractorTestingSupport } from '@angular/platform-browser';
import { AppComponent } from './app/app.component';
import { provideRouter } from '@angular/router';
import { routes } from './app/app.routes';
import { HTTP_INTERCEPTORS, provideHttpClient, withFetch, withInterceptors } from '@angular/common/http';
import { provideToastr, ToastrModule } from 'ngx-toastr';
import { jwtAuthInterceptor } from './app/interceptors/jwt-auth.interceptor';
import { provideAnimations } from '@angular/platform-browser/animations';

bootstrapApplication(AppComponent, {
  providers: [
    // {
    //   provide: HTTP_INTERCEPTORS,
    //   useClass: AuthHttpInterceptor,
    //   multi: true,
    // },
    provideProtractorTestingSupport(),
    provideRouter(routes),
    provideHttpClient(withFetch(), withInterceptors([jwtAuthInterceptor])),
    provideToastr({
        timeOut: 10000,
        positionClass: 'toast-bottom-right',
        preventDuplicates: true,
    })
    // importProvidersFrom(
    //   AuthModule.forRoot({
    //     ...environment.auth0,
    //     httpInterceptor: {
    //       allowedList: [`${environment.api.serverUrl}/api/messages/admin`, `${environment.api.serverUrl}/api/messages/protected`],
    //     },
    //   }),
    // ),
    ,
    provideAnimations()
],
}).catch((err) => console.error(err));
