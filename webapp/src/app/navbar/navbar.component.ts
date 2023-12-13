import { CommonModule } from '@angular/common';
import { Component, inject } from '@angular/core';
import { RouterLink, RouterOutlet } from '@angular/router';
import { AuthService } from '../services/auth.service';

@Component({
  selector: 'app-navbar',
  standalone: true,
  imports: [CommonModule, RouterLink, RouterOutlet],
  templateUrl: './navbar.component.html',
  styleUrl: './navbar.component.sass'
})
export class NavbarComponent {
  constructor(private authService: AuthService) {
  }

  userLoggedIn(): boolean {
    return this.authService.getUser();
  }

  handleLogin() {
    // this.auth.loginWithRedirect({
    //   appState: {
    //     target: '/gallery',
    //   },
    // });
  }
}
