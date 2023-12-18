import { CommonModule } from '@angular/common';
import { Component, EventEmitter, Input, Output } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { RouterLink, RouterOutlet } from '@angular/router';
import { ToastrService } from 'ngx-toastr';
import { Observable, of } from 'rxjs';
import { PostService } from '../services/post.service';
import { Post } from './post';

@Component({
  selector: 'app-post-card',
  standalone: true,
  imports: [CommonModule, RouterOutlet, RouterLink, FormsModule],
  templateUrl: './post-card.component.html',
  styleUrl: './post-card.component.sass'
})
export class PostCardComponent {
  @Input() postCard!: Post
  @Output() postUpdated = new EventEmitter<void>();
  userIsAdminOrOwner$: Observable<boolean> = of(false);

  constructor(private postService: PostService, private toastr: ToastrService) {
  }

  ngOnInit() {
    this.userIsAdminOrOwner$ = this.postService.checkAccessToPost(this.postCard._id);
  }

  deletePost() {
    this.postService.deletePost(this.postCard._id).subscribe({ 
      next: (response) => {
        this.showSuccessToast("Post deleted!");
        this.postUpdated.emit();
    }, 
      error: error => this.toastr.error(error.error.error)
    })
  }

  showSuccessToast(message: string) {
    this.toastr.success(message);
  }
}
