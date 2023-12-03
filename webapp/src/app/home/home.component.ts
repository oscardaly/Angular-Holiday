import { CommonModule } from '@angular/common';
import { Component, inject } from '@angular/core';
import { PostCardComponent } from '../post-card/post-card.component';
import { Post } from '../post-card/post';
import { PostService } from '../post.service';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [CommonModule, PostCardComponent],
  templateUrl: './home.component.html',
  styleUrl: './home.component.sass'
})

export class HomeComponent {
  postsList: Post[]  = [];
  postsService: PostService = inject(PostService);

  constructor() {
    this.postsList = this.postsService.getAllPosts();
  }
}
