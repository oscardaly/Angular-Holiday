import { HttpEventType, HttpInterceptorFn } from '@angular/common/http';
import { tap } from 'rxjs';

export const jwtAuthInterceptor: HttpInterceptorFn = (request, next) => {
  const token = JSON.parse(sessionStorage.getItem('token') ?? "")["token"];
  // const token = "123456"

  const modifiedRequest = request.clone({
    setHeaders:{
        // Authorization: `Bearer ${token}`
        "x-access-token": token
    }
  })

  return next(modifiedRequest).pipe(tap(event => {
    if (event.type === HttpEventType.Response) {
      console.log(modifiedRequest.url, 'returned a response with status', event.status);
    }
  }));;
};