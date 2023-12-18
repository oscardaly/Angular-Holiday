import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { FormControl, FormGroup, FormsModule, ReactiveFormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { ToastrService } from 'ngx-toastr';
import { AuthService } from '../services/auth.service';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './login.component.html',
  styleUrl: './login.component.sass'
})
export class LoginComponent {
  logInForm = new FormGroup({
    username: new FormControl(''),
    password: new FormControl('')
  });

  constructor(private authService: AuthService, private router: Router, private toastr: ToastrService) {}
  
  handleLogin() {
    if (this.logInForm.value.username && this.logInForm.value.password) {
      this.authService.login(this.logInForm.value.username ?? "", this.logInForm.value.password ?? "");
    }
  }
  
    showSuccessToast() {
      this.toastr.success("Logged in!");
    }
}