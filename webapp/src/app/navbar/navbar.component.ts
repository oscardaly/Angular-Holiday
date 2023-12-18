import { CommonModule } from '@angular/common';
import { Component, inject } from '@angular/core';
import { Router, RouterLink, RouterOutlet } from '@angular/router';
import { ToastrService } from 'ngx-toastr';
import { Observable, tap } from 'rxjs';
import { AuthService } from '../services/auth.service';
import { User } from '../services/user.service';

@Component({
  selector: 'app-navbar',
  standalone: true,
  imports: [CommonModule, RouterLink, RouterOutlet],
  templateUrl: './navbar.component.html',
  styleUrl: './navbar.component.sass'
})

export class NavbarComponent {
  currentUser$: Observable<User>;

  constructor(private authService: AuthService, private router: Router, private toastr: ToastrService) {
    this.currentUser$ = this.authService.getUser();
  }

  ngOnInit() {

  }

  userLoggedIn(): boolean {
    return this.authService.isUserLoggedIn();
  }

  logOut() {
    this.authService.logout()?.subscribe({ 
      next: (response) => {
        this.router.navigate(['/']);
        this.authService.deleteToken();
        this.showToast("Logged out!");
    }, 
      error: error => this.toastr.error(error.error.error)
    });
  }

  showToast(message: string) {
    this.toastr.success(message)
  };
}
