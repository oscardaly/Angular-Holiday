import { CommonModule } from '@angular/common';
import { Component, inject } from '@angular/core';
import { ActivatedRoute, RouterLink, RouterOutlet } from '@angular/router';
import { Observable } from 'rxjs/internal/Observable';
import { threadId } from 'worker_threads';
import { Post } from '../post-card/post';
import { PostCardComponent } from '../post-card/post-card.component';
import { PostService } from '../post.service';

@Component({
  selector: 'app-gallery',
  standalone: true,
  imports: [CommonModule, PostCardComponent, RouterLink, RouterOutlet],
  templateUrl: './gallery.component.html',
  styleUrl: './gallery.component.scss'
})
export class GalleryComponent {
  route: ActivatedRoute = inject(ActivatedRoute);
  posts: any;
  page: number = 1;
  page_size: number = 6;
  sort_by_direction: number = 1;
  sort_by_function: string = "_id";
  sortFunctions: string[] = ["Date", "Title", "City", "Country", "Comments"]
  
  constructor(public postService: PostService) {
    this.getParams();
    console.log("constructor")
    this.posts = this.postService.getPostsWithParams({pn: this.page, ps: this.page_size, sort_by_direction: this.sort_by_direction, sort_by_function: this.sort_by_function});
  }

  ngOnInit() {
    this.postService.refresh();
  }

  ViewMorePosts() {
    this.page_size += 6;
    this.posts = this.postService.getPostsWithParams({pn: this.page, ps: this.page_size, sort_by_direction: this.sort_by_direction, sort_by_function: this.sort_by_function});
  }

  OnChangeSort(sort_by_function: string) {
    this.sort_by_function = sort_by_function;
    this.posts = this.postService.getPostsWithParams({pn: this.page, ps: this.page_size, sort_by_direction: this.sort_by_direction, sort_by_function: this.sort_by_function});
  }

  getParams() {
    if (this.route.snapshot.params['pn']) {
      this.page = this.route.snapshot.params['pn'];
    }

    if (this.route.snapshot.params['ps']) {
      this.page_size = this.route.snapshot.params['ps'];
    }

    if (this.route.snapshot.params['sort_by_direction']) {
      this.sort_by_direction = this.route.snapshot.params['sort_by_direction'];
    }

    if (this.route.snapshot.params['sort_by_function']) {
      this.sort_by_function = this.route.snapshot.params['sort_by_function'];
    }
  }
}
