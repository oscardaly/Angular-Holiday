import { CommonModule } from '@angular/common';
import { Component, Input } from '@angular/core';
import { RouterLink, RouterOutlet } from '@angular/router';
import { Post } from './post';

@Component({
  selector: 'app-post-card',
  standalone: true,
  imports: [CommonModule, RouterOutlet, RouterLink],
  templateUrl: './post-card.component.html',
  styleUrl: './post-card.component.sass'
})
export class PostCardComponent {
  @Input() postCard!: Post
}
