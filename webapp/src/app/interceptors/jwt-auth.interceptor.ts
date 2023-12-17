import { HttpEventType, HttpInterceptorFn } from '@angular/common/http';
import { inject } from '@angular/core';
import { SsrCookieService } from 'ngx-cookie-service-ssr';
import { tap } from 'rxjs';
import { AuthService } from '../services/auth.service';


export const jwtAuthInterceptor: HttpInterceptorFn = (request, next) => {
  const authService = inject(AuthService)
  let token = authService.getToken();

  if (token) {
    token = JSON.parse(token)["token"];

    const modifiedRequest = request.clone({
      setHeaders:{
          // Authorization: `Bearer ${token}`
          "x-access-token": token ?? ""
      }
    })
  
    return next(modifiedRequest).pipe(tap(event => {
      if (event.type === HttpEventType.Response) {
        console.log(modifiedRequest.url, 'returned a response with status', event.status);
      }
    }));;
  }

  else {
    return next(request);
  }
};