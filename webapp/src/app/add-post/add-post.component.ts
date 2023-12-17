import { CommonModule } from '@angular/common';
import { Component, inject, Input } from '@angular/core';
import { FormControl, FormGroup, FormsModule, ReactiveFormsModule } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { NgSelectModule } from '@ng-select/ng-select';
import { ToastrService } from 'ngx-toastr';
import { Observable, of } from 'rxjs';
import { Post } from '../post-card/post';
import { CityService } from '../services/city.service';
import { PostService } from '../services/post.service';

@Component({
  selector: 'app-add-post',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, NgSelectModule, FormsModule],
  templateUrl: './add-post.component.html',
  styleUrl: './add-post.component.scss'
})

export class AddPostComponent {
  route: ActivatedRoute = inject(ActivatedRoute);

  postForm = new FormGroup({
    title: new FormControl(''),
    coverImage: new FormControl(''),
    description: new FormControl(''),
    text: new FormControl('')
  });

  country: string | undefined = undefined;
  city: string | undefined = undefined;
  cityPlaceholder: string = "Please select a country"
  cities$: Observable<string[]> = of([]);
  countries$: Observable<string[]>; 
  isCitiesFilterDisabled: boolean = true;
  cityID: string = "";
  title = "Create Post";

  constructor(private postService: PostService, private cityService: CityService, private router: Router, private toastr: ToastrService) {
    this.countries$ = this.cityService.getCountries();
    this.checkForEditFormat();
  }

  addPost() {
    this.cityService.getCityByName(this.city ?? "").subscribe(city => this.cityID = city.id);

    this.postService.addPost(
      this.postForm.value.title ?? '',
      this.postForm.value.coverImage ?? '',
      this.postForm.value.description ?? '',
      this.postForm.value.text ?? '',
      this.cityID ?? ""
    ).subscribe(response => {
      this.router.navigate(['/gallery']);
      this.showSuccessToast();
    });
  }

  checkForCountry() {
    if (this.country) {
      this.cityPlaceholder = "City";
      this.isCitiesFilterDisabled = false;
      this.cities$ = this.cityService.getCities(this.country);
    }

    else {
      this.city = undefined;
      this.cityPlaceholder = "Please select a country";
      this.isCitiesFilterDisabled = true;
    }
  }

  showSuccessToast() {
    if (this.title == "Add Post") {
      this.toastr.success("Post created!")
    }
    else {
      this.toastr.success("Post updated!")
    }
  }

  checkForEditFormat() {
    const postIDInUrl: string = this.route.snapshot.params['id'];

    if (postIDInUrl) {
      const postToEdit = this.postService.getPostByID(postIDInUrl);
      this.useEditPostFormat(postToEdit);
    }
  }

  useEditPostFormat(post: Observable<Post>) {
    post.subscribe(post => {
      this.postForm.controls["title"].setValue(post.title);
      this.postForm.controls["coverImage"].setValue(post.cover_photo);
      this.postForm.controls["description"].setValue(post.description);
      this.postForm.controls["text"].setValue(post.text);
      this.country = post.city.country;
      this.city = post.city.city_ascii;
      this.title = "Edit Post";
    })
  }
}
