import { Injectable } from '@angular/core';
import { Post } from './post-card/post';

@Injectable({
  providedIn: 'root'
})

export class PostService {
  posts: Post[] = [
    {
      id: 123,
      date: new Date(Date.now.toString()),
      coverImage: "/assets/background.jpg",
      title: "My trip to Edinburgh",
      description: "I had a class trip to the Christmas Markets",
      authorName: "Oscar Daly",
      authorUsername: "odaly",
      authorProfilePicture: "/assets/background.jpg",
      city: "Edinburgh",
      country: "Scotland"
    },
    {
      id: 234,
      date: new Date(Date.now.toString()),
      coverImage: "/assets/background.jpg",
      title: "My trip to Edinburgh",
      description: "I had a class trip to the Christmas Markets",
      authorName: "Oscar Daly",
      authorUsername: "odaly",
      authorProfilePicture: "/assets/background.jpg",
      city: "Edinburgh",
      country: "Scotland"
    },
    {
      id: 345,
      date: new Date(Date.now.toString()),
      coverImage: "/assets/background.jpg",
      title: "My trip to Edinburgh",
      description: "I had a class trip to the Christmas Markets",
      authorName: "Oscar Daly",
      authorUsername: "odaly",
      authorProfilePicture: "/assets/background.jpg",
      city: "Edinburgh",
      country: "Scotland"
    }
  ]

  getAllPosts(): Post[] {
    return this.posts;
  }

  getPostByID(id: number): Post | undefined {
    return this.posts.find((post) => post.id === id)
  }
}
