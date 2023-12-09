import { Routes } from '@angular/router';
import { AddPostComponent } from './add-post/add-post.component';
import { GalleryComponent } from './gallery/gallery.component';
import { HomeComponent } from './home/home.component';
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
    }
];