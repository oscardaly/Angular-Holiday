import { inject } from '@angular/core';
import { CanActivateFn } from '@angular/router';
import { ToastrService } from 'ngx-toastr';
import { Observable } from 'rxjs';
import { PostService } from '../services/post.service';

export const adminOrPostOwnerGuard: CanActivateFn = (route, state) => {
  const postService: PostService = inject(PostService);
  const toastr: ToastrService = inject(ToastrService);

  const access: Observable<boolean> = postService.checkAccessToPost(route.params['id'])
  return access;
}