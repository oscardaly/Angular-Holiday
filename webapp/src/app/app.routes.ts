import { Routes } from '@angular/router';
import { AddPostComponent } from './add-post/add-post.component';
import { GalleryComponent } from './gallery/gallery.component';
import { HomeComponent } from './home/home.component';
import { LoginComponent } from './login/login.component';
import { PageNotFoundComponent } from './page-not-found/page-not-found.component';
import { ProfileComponent } from './profile/profile.component';
import { adminOrPostOwnerGuard } from './root-guards/admin-or-post-owner.guard';
import { loggedInGuard } from './root-guards/logged-in.guard';
import { SignupComponent } from './signup/signup.component';
import { ViewPostComponent } from './view-post/view-post.component';

export const routes: Routes = [
    {
        path: '',
        component: HomeComponent,
        title: 'Home'
    },
    {
        path: 'gallery',
        component: GalleryComponent,
        title: 'Gallery'
    },
    {
        path: 'view-post/:id',
        component: ViewPostComponent,
        title: 'View Post'
    },
    {
        path: 'add-post',
        component: AddPostComponent,
        title: 'Add Post',
        canActivate: [loggedInGuard]
    },
    {
        path: 'edit-post/:id',
        component: AddPostComponent,
        title: 'Edit Post',
        canActivate: [adminOrPostOwnerGuard]
    },
    {
        path: 'login',
        component: LoginComponent,
        title: 'Login'
    },
    {
        path: 'signup',
        component: SignupComponent,
        title: 'Sign Up'
    },
    {
        path: 'profile',
        component: ProfileComponent,
        title: 'Profile',
        canActivate: [loggedInGuard]
    }, //needs to own the profile
    // {
    //     path: 'profile/posts',
    //     component: MyPostsComponent,
    //     title: 'My Posts'
    // }, //needs to be admin or account owner
    {
        path: '**',
        component: PageNotFoundComponent,
        title: 'Where\'s this?'
    }
];