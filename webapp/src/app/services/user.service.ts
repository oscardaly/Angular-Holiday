import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';

const BASEURL = "http://127.0.0.1:5000/api/v1.0/users";

@Injectable({
  providedIn: 'root'
})

export class UserService {
  constructor(private http: HttpClient) { 
  }

  getUserByUsername(username: string, token: string) {
    const baseHeaders = new HttpHeaders({
      'content-type': 'content/json',
      Authorization: `Bearer ${token}`});

    return this.http.get<User>(BASEURL + "/" + username, { headers: baseHeaders});
  }

  createUser(user: User) {
    const baseHeaders = new HttpHeaders().set('content-type', 'content/json');
    return this.http.post(BASEURL, JSON.stringify(user), { headers: baseHeaders});
  }

  updateUser(updatedUser: User, currentUsername: string) {
    const baseHeaders = new HttpHeaders().set('content-type', 'content/json');
    return this.http.put(BASEURL + "/" + currentUsername, JSON.stringify(updatedUser), { headers: baseHeaders});
  }

  deleteUser(username: string) {
    const baseHeaders = new HttpHeaders().set('content-type', 'content/json');
    return this.http.delete(BASEURL + "/" + username, { headers: baseHeaders});
  }
}

export interface User {
  _id?: string,
  username: string,
  forename: string,
  surname: string,
  password: string,
  profile_picture: string,
  admin?: boolean
};