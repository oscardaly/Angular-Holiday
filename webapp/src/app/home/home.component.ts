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
  constructor(public postService: PostService) {
  }

  ngOnInit() {
    this.postService.refresh();
  }
}
