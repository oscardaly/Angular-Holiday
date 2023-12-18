import { inject } from '@angular/core';
import { CanActivateFn, Router } from '@angular/router';
import { ToastrService } from 'ngx-toastr';
import { AuthService } from '../services/auth.service';

export const loggedInGuard: CanActivateFn = (route, state) => {
  const authService: AuthService = inject(AuthService);
  const router: Router = inject(Router);
  const toastr: ToastrService = inject(ToastrService);
  
  if (authService.isUserLoggedIn()) {
    return true;
  }

  else {
    router.navigate(['login']);
    toastr.error("You need to log in first!")
    return false;
  }
};
