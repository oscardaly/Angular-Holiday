import { Routes } from '@angular/router';
import { AddPostComponent } from './add-post/add-post.component';
import { GalleryComponent } from './gallery/gallery.component';
import { HomeComponent } from './home/home.component';
import { LoginComponent } from './login/login.component';
import { PageNotFoundComponent } from './page-not-found/page-not-found.component';
import { SignupComponent } from './signup/signup.component';
import { ViewPostComponent } from './view-post/view-post.component';

export const routes: Routes = [
    {
        path: '',
        component: HomeComponent,
        title: 'Home Page'
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
        title: 'Add Post'
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
        path: '**',
        component: PageNotFoundComponent,
        title: 'Where\'s this?'
    }
];