import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { PostCardComponent } from '../post-card/post-card.component';
import { PostService } from '../post.service';
import { RouterLink, RouterOutlet } from '@angular/router';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [CommonModule, PostCardComponent, RouterLink, RouterOutlet],
  templateUrl: './home.component.html',
  styleUrl: './home.component.sass'
})

export class HomeComponent implements OnInit {
  posts: any;
  constructor(public postService: PostService) {
  }

  ngOnInit() {
    this.posts = this.postService.getPostsWithParams({pn: 1, ps: 5, sort_by_direction: 1, sort_by_function: "_id"});
  }
}
