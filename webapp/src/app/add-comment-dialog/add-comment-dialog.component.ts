import { Component, Inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { MatDialogModule, MatDialogActions, MatDialogClose, MatDialogContent, MatDialogRef, MatDialogTitle, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
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
  comment: string = "";
  
  constructor(private postService: PostService,
    public dialogRef: MatDialogRef<AddCommentDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public postID: string
  ) {}

  onSubmit() {
    if (this.comment != "") {
      this.postService.addCommentToPost(this.comment, this.postID).subscribe(
        res => console.log(res)
      );
    }
  }

  onNoClick(): void {
    this.dialogRef.close();
  }
}
