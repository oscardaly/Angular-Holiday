import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { PostCardComponent } from '../post-card/post-card.component';
import { RouterLink, RouterOutlet } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { NgSelectModule } from '@ng-select/ng-select';
import { PostService } from '../services/post.service';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [CommonModule, PostCardComponent, RouterLink, RouterOutlet, FormsModule, NgSelectModule],
  templateUrl: './home.component.html',
  styleUrl: './home.component.sass'
})

export class HomeComponent implements OnInit {
  posts: any;
  title: string | undefined = undefined;

  constructor(public postService: PostService) {
  }

  ngOnInit() {
    this.getPosts();
  }

  getPosts() {
    this.posts = this.postService.getPostsWithParams({pn: 1, ps: 5, sort_by_direction: 1, sort_by_function: "_id"});
  }
}
