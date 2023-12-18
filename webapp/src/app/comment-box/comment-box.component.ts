import { CommonModule } from '@angular/common';
import { Component, EventEmitter, Input, Output } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { Router } from '@angular/router';
import { ToastrService } from 'ngx-toastr';
import { AddCommentDialogComponent } from '../add-comment-dialog/add-comment-dialog.component';
import { Comment } from '../post-card/comment'
import { PostService } from '../services/post.service';

@Component({
  selector: 'app-comment-box',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './comment-box.component.html',
  styleUrl: './comment-box.component.sass'
})
export class CommentBoxComponent {
  @Input() comment!: Comment;
  @Input() postID!: string;
  @Output() commentDeleted = new EventEmitter<void>();

  constructor(public postService: PostService, private router: Router, private toastr: ToastrService, public dialog: MatDialog) {
  }

  deleteComment() {
    this.postService.deleteComment(this.postID, this.comment._id).subscribe({ 
      next: (response) => {
        this.showSuccessToast("Comment deleted!");
        this.commentDeleted.emit();
    }, 
      error: error => this.toastr.error(error.error.error)
    });
  }

  editComment() {
    const dialogRef = this.dialog.open(AddCommentDialogComponent, {
      data: { comment: this.comment.text, commentID: this.comment._id, postID: this.postID},
      height: '400px',
      width: '600px',
    });

    dialogRef.afterClosed().subscribe(result => {
      this.commentDeleted.emit();
    });
  }

  showSuccessToast(message: string) {
    this.toastr.success(message);
  }
}
