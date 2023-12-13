import { CommonModule } from '@angular/common';
import { Component, inject } from '@angular/core';
import { FormControl, FormGroup, FormsModule, ReactiveFormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { NgSelectModule } from '@ng-select/ng-select';
import { ToastrService } from 'ngx-toastr';
import { Observable, of } from 'rxjs';
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

  constructor(private postService: PostService, private cityService: CityService, private router: Router, private toastr: ToastrService) {
    this.countries$ = this.cityService.getCountries();
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
      this.router.navigate(['/']);
      this.showSuccessToast();
    });
  }

checkForCountry() {
  console.log(this.country);

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
  this.toastr.success("Post created!")
}
}
