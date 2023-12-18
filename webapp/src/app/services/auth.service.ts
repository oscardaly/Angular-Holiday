import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { jwtDecode } from 'jwt-decode';
import { EMPTY, EmptyError, tap } from 'rxjs';
import { User, UserService } from './user.service';
import { SsrCookieService } from 'ngx-cookie-service-ssr';
import { ToastrService } from 'ngx-toastr';
import { Router } from '@angular/router';

const BASEURL = "http://127.0.0.1:5000/api/v1.0/";

@Injectable({
  providedIn: 'root'
})

export class AuthService {
  constructor(private http: HttpClient, private userService: UserService, private cookieService: SsrCookieService, private toastr: ToastrService, private router: Router) { 
  }

  isUserLoggedIn() {
    return this.cookieService.check('token');
  }

  getUser() {
    const token = this.cookieService.get('token');

    try {
      const user: TokenData = jwtDecode(JSON.stringify(token));
      return this.userService.getUserByUsername(user.username, token);
    }
    
    catch {
      return EMPTY;
    }
  }

  getToken() {
    return this.cookieService.get('token');
  }

  deleteToken() {
    this.cookieService.delete('token')
  }

  login(username: string, password: string) {
    const baseHeaders = new HttpHeaders()
    .set('content-type', 'content/json')
    .set("Authorization", "Basic " + btoa(`${username}:${password}`));
    return this.http.get<string>(BASEURL + "login", { headers: baseHeaders})
    .subscribe({
      next: token => {
        this.cookieService.set('token', JSON.stringify(token), { expires: 120});
        this.router.navigate(['/']);
        this.toastr.success("Logged in!");
      },
      error: error => this.toastr.error(error.error.message)
    });
  }

  logout() {
    const token = this.cookieService.get('token');
    
    if (token != "") {
      const baseHeaders = new HttpHeaders()
      .set('content-type', 'content/json')
      .set("x-access-token", token);

      return this.http.get<string>(BASEURL + "logout", { headers: baseHeaders});
    }

    return undefined;
  }
}

export interface TokenData {
  username: string,
  admin: boolean,
  exp:  number
}