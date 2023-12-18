import { CommonModule } from '@angular/common';
import { Component, inject, OnInit } from '@angular/core';
import { GoogleMapsModule } from '@angular/google-maps';
import { ActivatedRoute, RouterLink, RouterOutlet } from '@angular/router';
import { Observable } from 'rxjs';
import { CommentBoxComponent } from '../comment-box/comment-box.component';
import { Post } from '../post-card/post';
import { Comment } from '../post-card/comment';
import { PostService } from '../services/post.service';
import { MatDialog } from '@angular/material/dialog'
import { AddCommentDialogComponent } from '../add-comment-dialog/add-comment-dialog.component';
import { AuthService } from '../services/auth.service';
import { ToastrService } from 'ngx-toastr';

@Component({
  selector: 'app-view-post',
  standalone: true,
  imports: [CommonModule, RouterLink, RouterOutlet, GoogleMapsModule, CommentBoxComponent],
  templateUrl: './view-post.component.html',
  styleUrl: './view-post.component.sass'
})
export class ViewPostComponent implements OnInit {
  route: ActivatedRoute = inject(ActivatedRoute);
  post$: Observable<Post>;
  postID: string = "";
  comments: Comment[] = [];
  page: number = 1;
  page_size: number = 3;
  sort_by_direction: number = 1;

  constructor(public postService: PostService, public dialog: MatDialog, private authService: AuthService, private toastr: ToastrService) {
    this.postID = this.route.snapshot.params['id'];
    this.post$ = this.postService.getPostByID(this.postID);
    this.getCommentsForPost(this.postID); 
  }

  ngOnInit() {
  }

  getCentre(lat: number, lng: number) {
    return new google.maps.LatLng(lat, lng);
  }

  getCommentsForPost(postID: string) {
    this.postService.getCommentsOnPost(postID, this.page, this.page_size, this.sort_by_direction).subscribe(comments => this.comments = comments);
  }

  swapSortDirection() {
    if (this.sort_by_direction == 1) {
      this.sort_by_direction = -1
    } 
    else {
      this.sort_by_direction = 1
    } 

    this.getCommentsForPost(this.postID);
  }

  displayViewMoreButton(): boolean {
    if (this.comments.length > 0 && this.comments.length % 3 == 0) {
      return true;
    }
    
    else {
      return false;
    }
  }

  ViewMorePosts() {
    this.page_size += 3;
    this.getCommentsForPost(this.postID);
  }


  openModal() {
    if (this.authService.isUserLoggedIn()) {
      const dialogRef = this.dialog.open(AddCommentDialogComponent, {
        data: { comment: "", postID: this.postID},
        height: '400px',
        width: '600px',
      });
  
      dialogRef.afterClosed().subscribe(result => {
        this.getCommentsForPost(this.postID);
      });
    }
    
    else {
      this.toastr.error("You must be logged in to add a comment!")
    }
  }
}


//dont do aync work in constructor do it in OnInit 
// obseravles use $ after variable name