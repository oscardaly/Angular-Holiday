import { Component, Inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { MatDialogModule, MatDialogActions, MatDialogClose, MatDialogContent, MatDialogRef, MatDialogTitle, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { ToastrService } from 'ngx-toastr';
import { PostService } from '../services/post.service';

@Component({
  selector: 'app-add-comment-dialog',
  standalone: true,
  imports: [
    MatDialogModule,
    FormsModule,
    MatDialogTitle,
    MatDialogContent,
    MatDialogActions,
    MatDialogClose,
    MatFormFieldModule,
    MatInputModule
  ],
  templateUrl: './add-comment-dialog.component.html',
  styleUrl: './add-comment-dialog.component.scss'
})
export class AddCommentDialogComponent {  
  title: string = "Add Comment";
  submitButtonText = "Add"

  constructor(private postService: PostService,
    public dialogRef: MatDialogRef<AddCommentDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: DialogData,
    private toastr: ToastrService
  ) {
    if (data.comment != "") {
      this.title = "Edit comment";
      this.submitButtonText = "Edit"
    }
  }

  onSubmit() {
    if (this.data.comment != "" && this.submitButtonText == "Edit") {
      this.postService.editComment(this.data.commentID ?? "", this.data.comment).subscribe({ 
        next: (response) => this.showSuccessToast("Comment updated!"), 
        error: error => this.toastr.error(error.error.error)
      });
    }

    else if (this.data.comment != "" && this.submitButtonText == "Add") {
      this.postService.addCommentToPost(this.data.comment, this.data.postID).subscribe({
        next: (response) => this.showSuccessToast("Comment added!"), 
        error: error => this.toastr.error(error.error.error)
      });
    }
  }

  onNoClick(): void {
    this.dialogRef.close();
  }

  showSuccessToast(message: string) {
    this.toastr.success(message);
  }
}

export type DialogData = {
  comment: string, 
  commentID?: string,
  postID: string
}
