import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { FormControl, FormGroup, FormsModule, ReactiveFormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { ToastrService } from 'ngx-toastr';
import { Observable, tap } from 'rxjs';
import { AuthService } from '../services/auth.service';
import { User, UserService } from '../services/user.service';

@Component({
  selector: 'app-profile',
  standalone: true,
  imports: [CommonModule, FormsModule, ReactiveFormsModule],
  templateUrl: './profile.component.html',
  styleUrl: './profile.component.scss'
})
export class ProfileComponent {
  user$: Observable<User>;
  userForm = new FormGroup({
    forename: new FormControl(''),
    surname: new FormControl(''),
    username: new FormControl(''),
    password: new FormControl(''),
    profile_picture: new FormControl(''),
  });
  
  constructor(private authService: AuthService, private userService: UserService, private toastr: ToastrService, private router: Router) {
    this.user$ = this.authService.getUser();

    this.user$.subscribe(user => {
      this.userForm.controls["forename"].setValue(user.forename);
      this.userForm.controls["surname"].setValue(user.surname);
      this.userForm.controls["username"].setValue(user.username);
      this.userForm.controls["password"].setValue(user.password);
      this.userForm.controls["profile_picture"].setValue(user.profile_picture);
    })
  }

  updateUser() {
    this.user$.subscribe(currentUser => {
      this.userService.updateUser({
        forename: this.userForm.value.forename ?? '',
        surname: this.userForm.value.surname ?? '',
        username: this.userForm.value.username ?? '',
        password: this.userForm.value.password ?? '',
        profile_picture: this.userForm.value.profile_picture ?? ''
      },
        currentUser.username)
        .subscribe({ 
          next: (response) => {
            this.authService.logout();
            this.authService.login(this.userForm.value.username ?? "", this.userForm.value.password ?? "")
            this.showSuccessToast("User updated!");
        }, 
          error: error => this.toastr.error(error.error.error)
        });
    })
  }

  deleteUser() {
    this.user$.subscribe(currentUser => {
      this.userService.deleteUser(currentUser.username)
        .subscribe({ 
          next: (response) => {
            this.authService.logout();
            this.authService.deleteToken();
            this.router.navigate(['/']);
            this.showSuccessToast("Account deleted!");
        }, 
          error: error => this.toastr.error(error.error.error)
        });
    })
  }

  showSuccessToast(message: string) {
    this.toastr.success(message)
  }
}
