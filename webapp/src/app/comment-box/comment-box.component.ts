import { CommonModule } from '@angular/common';
import { Component, Input } from '@angular/core';
import { Comment } from '../post-card/comment'

@Component({
  selector: 'app-comment-box',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './comment-box.component.html',
  styleUrl: './comment-box.component.sass'
})
export class CommentBoxComponent {
  @Input() comment!: Comment;

  constructor() {
  }
}
