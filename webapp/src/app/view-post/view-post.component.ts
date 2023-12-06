import { CommonModule } from '@angular/common';
import { Component, inject, Input } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { PostService } from '../post.service';

@Component({
  selector: 'app-view-post',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './view-post.component.html',
  styleUrl: './view-post.component.sass'
})
export class ViewPostComponent {
  route: ActivatedRoute = inject(ActivatedRoute);
  post: any;

  constructor(public postService: PostService) {
    const postID = this.route.snapshot.params['id'];
    this.post = this.postService.getPostByID(postID);
    console.log(this.post)
  }
}
