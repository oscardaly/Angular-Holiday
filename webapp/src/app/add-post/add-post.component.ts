import { CommonModule } from '@angular/common';
import { Component, inject } from '@angular/core';
import { FormControl, FormGroup, ReactiveFormsModule } from '@angular/forms';
import { PostService } from '../post.service';

@Component({
  selector: 'app-add-post',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './add-post.component.html',
  styleUrl: './add-post.component.scss'
})

export class AddPostComponent {
  postService = inject(PostService);
  postForm = new FormGroup({
    title: new FormControl(''),
    coverImage: new FormControl(''),
    description: new FormControl(''),
    text: new FormControl(''),
    city: new FormControl('')
  });

  constructor() {}

  addPost() {
    this.postService.addPost(
      this.postForm.value.title ?? '',
      this.postForm.value.coverImage ?? '',
      this.postForm.value.description ?? '',
      this.postForm.value.text ?? '',
      Number(this.postForm.value.city) ?? -1
    );
  }
}
