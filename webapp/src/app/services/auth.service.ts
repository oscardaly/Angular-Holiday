import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { jwtDecode } from 'jwt-decode';
import { User, UserService } from './user.service';

const BASEURL = "http://127.0.0.1:5000/api/v1.0/login";

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  user: User | undefined;
  number: number = 1;

  constructor(private http: HttpClient, private userService: UserService) { 
  }

  getUser() {
    // try {
    //   const token = sessionStorage.getItem('token');

    //   if (token && this.number <= 3) {
    //     const user: TokenData = jwtDecode(JSON.stringify(token));
    //     this.number += 1;
    //     console.log(user.username);
    //     this.userService.getUserByUsername(user.username, token).subscribe(user => this.user = user);
    //     console.log(this.user)
    //   }
    // }
    // finally {
    //   return this.user;
    // }
    return false
  }

  login(username: string, password: string) {
    const baseHeaders = new HttpHeaders()
    .set('content-type', 'content/json')
    .set("Authorization", "Basic " + btoa(`${username}:${password}`));
    console.log(username + password)
    return this.http.get<string>(BASEURL, { headers: baseHeaders})
    .subscribe(token => sessionStorage.setItem('token', JSON.stringify(token)));
  }

  logout() {
    const token = sessionStorage.getItem('token');
    
    if (token) {
      const baseHeaders = new HttpHeaders()
      .set('content-type', 'content/json')
      .set("x-access-token", token);

      this.user = undefined;

      return this.http.get<string>(BASEURL, { headers: baseHeaders});
    }

    return "";
  }
}

export interface TokenData {
  username: string,
  admin: boolean,
  exp:  number
}