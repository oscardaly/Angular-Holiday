import { CommonModule } from '@angular/common';
import { Component, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, RouterLink, RouterOutlet } from '@angular/router';
import { NgSelectModule } from '@ng-select/ng-select';
import { Observable, of } from 'rxjs';
import { Post } from '../post-card/post';
import { PostCardComponent } from '../post-card/post-card.component';
import { CityService } from '../services/city.service';
import { PostService } from '../services/post.service';

@Component({
  selector: 'app-gallery',
  standalone: true,
  imports: [CommonModule, PostCardComponent, RouterLink, RouterOutlet, NgSelectModule, FormsModule],
  templateUrl: './gallery.component.html',
  styleUrl: './gallery.component.scss'
})

export class GalleryComponent {
  route: ActivatedRoute = inject(ActivatedRoute);
  posts: Post[] = []
  title: string | undefined = undefined;
  country: string | undefined = undefined;
  city: string | undefined = undefined;
  cityPlaceholder: string = "Please select a country"
  page: number = 1;
  page_size: number = 6;
  sort_by_direction: number = 1;
  sort_by_function: string = "_id";
  sortFunctions: string[] = ["Date", "Title", "City", "Country", "Comments"]
  cities$: Observable<string[]> = of([]);
  countries$: Observable<string[]>; 
  isCitiesFilterDisabled: boolean = true;
  
  constructor(public postService: PostService, public cityService: CityService) {
    this.getUrlParams();
    this.getPosts();
    this.countries$ = this.cityService.getCountries();
  }

  getPosts() {
    this.postService.getPostsWithParams({pn: this.page, ps: this.page_size, sort_by_direction: this.sort_by_direction, sort_by_function: this.sort_by_function, city: this.city, country: this.country, title: this.title})
    .subscribe(posts => this.posts = posts);
  }

  ViewMorePosts() {
    this.page_size += 6;
    this.getPosts();
    }

  OnChangeSort(sort_by_function: string) {
    this.sort_by_function = sort_by_function;
    this.getPosts();
    }
  
    swapSortDirection() {
      if (this.sort_by_direction == 1) {
        this.sort_by_direction = -1
      } 
      else {
        this.sort_by_direction = 1
      } 
  
      this.getPosts();
    }
  
    onCloseCountryFilter() {
      this.checkForCountry();
      this.getPosts();
    }
  
    onClearFilter() {
      this.checkForCountry();
      this.getPosts();
    }

  checkForCountry() {
    if (this.country) {
      this.cityPlaceholder = "City";
      this.isCitiesFilterDisabled = false;
      this.cities$ = this.cityService.getCities(this.country);
      this.updateRoute("country", this.country);
    }

    else {
      this.city = undefined;
      this.cityPlaceholder = "Please select a country";
      this.isCitiesFilterDisabled = true;
    }
  }

  updateRoute(paramName: string, value: string) {
    // this.route.queryParams.navigate([], {
    //   queryParams[paramName] = value;
    //   queryParamsHandling: 'merge'
    // });
  }

  displayViewMoreButton(): boolean {
    if (this.posts.length >= 6) {
      return true;
    }
    
    else {
      return false;
    }
  }

  getUrlParams() {
    this.route.queryParamMap.subscribe(params => {
      const countryParam = params.get('country');
      const cityParam = params.get('city');
      const titleParam = params.get('title');

      if (countryParam) {
        this.country = countryParam;
      }

      if (cityParam) {
        this.city = cityParam;
      }

      if (titleParam) {
        this.title = titleParam;
      }
    });
  }
}
