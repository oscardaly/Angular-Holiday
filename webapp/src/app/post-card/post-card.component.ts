import { CommonModule } from '@angular/common';
import { Component, Input } from '@angular/core';
import { Post } from './post';

@Component({
  selector: 'app-post-card',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './post-card.component.html',
  styleUrl: './post-card.component.sass'
})
export class PostCardComponent {
  @Input() postCard!: Post
}
