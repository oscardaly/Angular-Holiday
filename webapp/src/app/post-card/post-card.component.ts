import { CommonModule } from '@angular/common';
import { Component, EventEmitter, Input, Output } from '@angular/core';
import { RouterLink, RouterOutlet } from '@angular/router';
import { ToastrService } from 'ngx-toastr';
import { PostService } from '../services/post.service';
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
  @Output() postUpdated = new EventEmitter<void>();

  constructor(private postService: PostService, private toastr: ToastrService) {}

  deletePost() {
    this.postService.deletePost(this.postCard._id).subscribe(response => {
      this.showSuccessToast("Post deleted!");
      this.postUpdated.emit();
    })
  }

  showSuccessToast(message: string) {
    this.toastr.success(message);
  }
}
