import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { FormControl, FormGroup, ReactiveFormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { ToastrService } from 'ngx-toastr';
import { UserService } from '../services/user.service';

@Component({
  selector: 'app-signup',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './signup.component.html',
  styleUrl: './signup.component.sass'
})

export class SignupComponent {
  signUpForm = new FormGroup({
    username: new FormControl(''),
    forename: new FormControl(''),
    surname: new FormControl(''),
    password: new FormControl(''),
    profile_picture: new FormControl('')
  });
  
  constructor(private userService: UserService, private router: Router, private toastr: ToastrService) {}
  
  handleSignUp() {
    this.userService.createUser({
      username: this.signUpForm.value.username ?? '',
      forename: this.signUpForm.value.forename ?? '',
      surname: this.signUpForm.value.surname ?? '',
      password: this.signUpForm.value.password ?? '',
      profile_picture: this.signUpForm.value.profile_picture ?? ''
    }).subscribe(response => {
      this.signUpForm.reset()
      this.router.navigate(['/']);
      this.showSuccessToast();
    });
  }

  showSuccessToast() {
    this.toastr.success("Account created!")
  }
}
