import { CommonModule } from '@angular/common';
import { Component, inject, OnInit } from '@angular/core';
import { ActivatedRoute, RouterLink, RouterOutlet } from '@angular/router';
import { Observable, tap } from 'rxjs';
import { Post } from '../post-card/post';
import { PostService } from '../post.service';

@Component({
  selector: 'app-view-post',
  standalone: true,
  imports: [CommonModule, RouterLink, RouterOutlet],
  templateUrl: './view-post.component.html',
  styleUrl: './view-post.component.sass'
})
export class ViewPostComponent implements OnInit {
  route: ActivatedRoute = inject(ActivatedRoute);
  post$: Observable<Post>;

  constructor(public postService: PostService) {
    const postID: string = this.route.snapshot.params['id'];
    this.post$ = this.postService.getPostByID(postID)
  }

  ngOnInit() {
    // const postID: string = this.route.snapshot.params['id'];
    // this.postService.getPostByID(postID);
    // .subscribe(post => this.post = post);
  }
}


//dont do aync work in constructor do it in OnInit 
// obseravles use $ after variable name