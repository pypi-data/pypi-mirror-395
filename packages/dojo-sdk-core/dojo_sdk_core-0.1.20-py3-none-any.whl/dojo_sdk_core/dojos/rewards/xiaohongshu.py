"""
Reward functions for Xiaohongshu (Little Red Book) app tasks.
"""

import logging
from typing import Any, Dict, Optional, Tuple

logger = logging.getLogger(__name__)


def _find_post(final_state: Dict[str, Any], post_id: str) -> Tuple[Optional[Dict[str, Any]], str]:
    posts = final_state.get("posts")
    if not isinstance(posts, list):
        return None, "Posts array missing in final state"
    for post in posts:
        if post.get("id") == post_id:
            return post, ""
    return None, f"Post with id '{post_id}' not found in final state"


def _find_comment(post: Dict[str, Any], comment_id: str) -> Tuple[Optional[Dict[str, Any]], str]:
    comments = post.get("comments")
    if not isinstance(comments, list):
        return None, f"Post {post.get('id')} comments array missing"
    for comment in comments:
        if comment.get("id") == comment_id:
            return comment, ""
    return None, f"Comment '{comment_id}' not found on post {post.get('id')}"


def _find_user(final_state: Dict[str, Any], user_id: str) -> Tuple[Optional[Dict[str, Any]], str]:
    users = final_state.get("users")
    if not isinstance(users, list):
        return None, "Users array missing in final state"
    for user in users:
        if user.get("id") == user_id:
            return user, ""
    return None, f"User with id '{user_id}' not found in final state"


def _get_current_user(final_state: Dict[str, Any]) -> Tuple[Optional[Dict[str, Any]], str]:
    current_user = final_state.get("currentUser")
    if not isinstance(current_user, dict):
        return None, "currentUser object missing in final state"
    return current_user, ""


def _find_album_by_name(user: Dict[str, Any], album_name: str) -> Tuple[Optional[Dict[str, Any]], str]:
    albums = user.get("albums")
    if not isinstance(albums, list):
        return None, "currentUser.albums missing or not a list"
    for album in albums:
        if album.get("name") == album_name:
            return album, ""
    return None, f"Album named '{album_name}' not found for current user"


def _validate_single_comment(
    post: Dict[str, Any], expected_text: str, *, expected_author: Optional[str] = None
) -> Tuple[bool, str]:
    comments = post.get("comments")
    if not isinstance(comments, list):
        return False, f"Post {post.get('id')} comments array missing"
    if len(comments) != 1:
        return False, f"Post {post.get('id')} has {len(comments)} comments, expected 1"
    comment = comments[0]
    content = comment.get("content", "")
    if expected_text.lower() not in content.lower():
        return False, f"Post {post.get('id')} comment content '{content}' missing '{expected_text}'"
    if expected_author is not None and comment.get("authorId") != expected_author:
        return False, f"Post {post.get('id')} comment authorId={comment.get('authorId')} expected {expected_author}"
    return True, ""


def _check_exact_list(values: Any, expected: Tuple[str, ...], field_name: str) -> Tuple[bool, str]:
    if not isinstance(values, list):
        return False, f"{field_name} is not a list"
    if len(values) != len(expected):
        return False, f"{field_name} has length {len(values)}, expected {len(expected)}"
    if sorted(values) != sorted(expected):
        return False, f"{field_name}={values} does not match expected {list(expected)}"
    return True, ""


def _validate_bookmarkpost(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    current_user, error = _get_current_user(final_state)
    if not current_user:
        return 0.0, error

    ok, error = _check_exact_list(current_user.get("bookmarks"), ("1",), "currentUser.bookmarks")
    if not ok:
        return 0.0, error

    post, error = _find_post(final_state, "1")
    if not post:
        return 0.0, error
    if post.get("bookmarks") != 1:
        return 0.0, f"Post 1 bookmarks={post.get('bookmarks')} expected 1"

    user, error = _find_user(final_state, "1")
    if not user:
        return 0.0, error
    if user.get("bookmarkedCount") != 1:
        return 0.0, f"User 1 bookmarkedCount={user.get('bookmarkedCount')} expected 1"

    return 1.0, "Post 1 bookmarked and counts updated"


def _validate_commentontwoseparateposts(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    post1, error = _find_post(final_state, "1")
    if not post1:
        return 0.0, error
    ok, error = _validate_single_comment(post1, "nice song!")
    if not ok:
        return 0.0, error

    post2, error = _find_post(final_state, "2")
    if not post2:
        return 0.0, error
    ok, error = _validate_single_comment(post2, "what the dog doing?")
    if not ok:
        return 0.0, error

    if final_state.get("page") != "explore":
        return 0.0, f"page is {final_state.get('page')} expected 'explore'"

    return 1.0, "Posted correct comments on posts 1 and 2 while staying on explore page"


def _validate_commentonvideo(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    post, error = _find_post(final_state, "4")
    if not post:
        return 0.0, error
    ok, error = _validate_single_comment(post, "this cat so cute!", expected_author="0")
    if not ok:
        return 0.0, error
    return 1.0, "Successfully commented 'this cat so cute!' on post 4"


def _validate_comprehensiveuserinteraction(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    if final_state.get("page") != "explore":
        return 0.0, f"page is {final_state.get('page')} expected 'explore'"

    post1, error = _find_post(final_state, "1")
    if not post1:
        return 0.0, error
    if post1.get("likes") != 1:
        return 0.0, f"Post 1 likes={post1.get('likes')} expected 1"
    ok, error = _validate_single_comment(post1, "nice")
    if not ok:
        return 0.0, error

    post2, error = _find_post(final_state, "2")
    if not post2:
        return 0.0, error
    if post2.get("likes") != 1 or post2.get("bookmarks") != 1:
        return 0.0, f"Post 2 likes={post2.get('likes')} bookmarks={post2.get('bookmarks')} expected 1/1"

    post7, error = _find_post(final_state, "7")
    if not post7:
        return 0.0, error
    if post7.get("likes") != 1:
        return 0.0, f"Post 7 likes={post7.get('likes')} expected 1"

    user1, error = _find_user(final_state, "1")
    if not user1:
        return 0.0, error
    if user1.get("likeCount") != 1:
        return 0.0, f"User 1 likeCount={user1.get('likeCount')} expected 1"

    user2, error = _find_user(final_state, "2")
    if not user2:
        return 0.0, error
    if user2.get("likeCount") != 2 or user2.get("bookmarkedCount") != 1:
        return 0.0, (f"User 2 likeCount={user2.get('likeCount')} bookmarkedCount={user2.get('bookmarkedCount')} expected 2/1")

    current_user, error = _get_current_user(final_state)
    if not current_user:
        return 0.0, error
    ok, error = _check_exact_list(current_user.get("likedPosts"), ("1", "2", "7"), "currentUser.likedPosts")
    if not ok:
        return 0.0, error
    ok, error = _check_exact_list(current_user.get("following"), ("2",), "currentUser.following")
    if not ok:
        return 0.0, error

    return 1.0, "Completed comprehensive multi-post interaction requirements"


def _validate_crossuserengagement(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    post_ids = {
        "1": {"likes": 1},
        "2": {"likes": 1, "bookmarks": 1},
        "3": {"likes": 1},
        "4": {"likes": 1, "bookmarks": 1},
        "5": {"likes": 1},
    }

    for pid, expectations in post_ids.items():
        post, error = _find_post(final_state, pid)
        if not post:
            return 0.0, error
        for field, expected_value in expectations.items():
            if post.get(field) != expected_value:
                return 0.0, f"Post {pid} {field}={post.get(field)} expected {expected_value}"

    post3, _ = _find_post(final_state, "3")
    ok, error = _validate_single_comment(post3, "nice")
    if not ok:
        return 0.0, error

    post4, _ = _find_post(final_state, "4")
    ok, error = _validate_single_comment(post4, "meow")
    if not ok:
        return 0.0, error

    user5, error = _find_user(final_state, "5")
    if not user5:
        return 0.0, error
    followers = user5.get("followers")
    if not isinstance(followers, list) or "0" not in followers:
        return 0.0, f"User 5 followers={followers} expected to include '0'"

    if final_state.get("page") != "profile" or final_state.get("profileUserId") != "5":
        return 0.0, (f"page={final_state.get('page')} profileUserId={final_state.get('profileUserId')} expected profile/5")

    return 1.0, "Completed cross-user engagement interactions and viewed user 5 profile"


def _validate_follownavigatehome(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    current_user, error = _get_current_user(final_state)
    if not current_user:
        return 0.0, error
    following = current_user.get("following")
    if not isinstance(following, list) or "2" not in following:
        return 0.0, f"currentUser.following={following} expected to include '2'"

    user2, error = _find_user(final_state, "2")
    if not user2:
        return 0.0, error
    followers = user2.get("followers")
    if not isinstance(followers, list) or "0" not in followers:
        return 0.0, f"User 2 followers={followers} expected to include '0'"

    if final_state.get("page") != "explore":
        return 0.0, f"page is {final_state.get('page')} expected 'explore'"

    return 1.0, "Followed user 2 and returned to explore page"


def _validate_followuser(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    current_user, error = _get_current_user(final_state)
    if not current_user:
        return 0.0, error
    ok, err = _check_exact_list(current_user.get("following"), ("1",), "currentUser.following")
    if not ok:
        return 0.0, err

    user1, error = _find_user(final_state, "1")
    if not user1:
        return 0.0, error
    ok, err = _check_exact_list(user1.get("followers"), ("0",), "User 1 followers")
    if not ok:
        return 0.0, err

    return 1.0, "Successfully followed user 1"


def _validate_like3sequential(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    for pid in ("1", "2", "3"):
        post, error = _find_post(final_state, pid)
        if not post:
            return 0.0, error
        if post.get("likes") != 1:
            return 0.0, f"Post {pid} likes={post.get('likes')} expected 1"

    current_user, error = _get_current_user(final_state)
    if not current_user:
        return 0.0, error
    ok, err = _check_exact_list(current_user.get("likedPosts"), ("1", "2", "3"), "currentUser.likedPosts")
    if not ok:
        return 0.0, err

    for uid in ("1", "2", "3"):
        user, error = _find_user(final_state, uid)
        if not user:
            return 0.0, error
        if user.get("likeCount") != 1:
            return 0.0, f"User {uid} likeCount={user.get('likeCount')} expected 1"

    return 1.0, "Sequentially liked posts 1, 2, and 3"


def _validate_likeandbookmark(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    post, error = _find_post(final_state, "2")
    if not post:
        return 0.0, error
    if post.get("likes") != 1 or post.get("bookmarks") != 1:
        return 0.0, f"Post 2 likes={post.get('likes')} bookmarks={post.get('bookmarks')} expected 1/1"

    user2, error = _find_user(final_state, "2")
    if not user2:
        return 0.0, error
    if user2.get("likeCount") != 1 or user2.get("bookmarkedCount") != 1:
        return 0.0, (f"User 2 likeCount={user2.get('likeCount')} bookmarkedCount={user2.get('bookmarkedCount')} expected 1/1")

    current_user, error = _get_current_user(final_state)
    if not current_user:
        return 0.0, error
    ok, err = _check_exact_list(current_user.get("likedPosts"), ("2",), "currentUser.likedPosts")
    if not ok:
        return 0.0, err
    ok, err = _check_exact_list(current_user.get("bookmarks"), ("2",), "currentUser.bookmarks")
    if not ok:
        return 0.0, err

    return 1.0, "Liked and bookmarked post 2 with correct counts"


def _validate_likepost(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    post, error = _find_post(final_state, "1")
    if not post:
        return 0.0, error
    if post.get("likes") != 1:
        return 0.0, f"Post 1 likes={post.get('likes')} expected 1"

    user1, error = _find_user(final_state, "1")
    if not user1:
        return 0.0, error
    if user1.get("likeCount") != 1:
        return 0.0, f"User 1 likeCount={user1.get('likeCount')} expected 1"

    return 1.0, "Liked post 1"


def _validate_navigateownprofile(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    if final_state.get("page") != "profile":
        return 0.0, f"page is {final_state.get('page')} expected 'profile'"
    if final_state.get("profileUserId") != "0":
        return 0.0, f"profileUserId={final_state.get('profileUserId')} expected '0'"
    return 1.0, "Navigated to current user's profile"


def _validate_openpostmodal(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    if not final_state.get("activePostId"):
        return 0.0, "activePostId is missing or null"
    if final_state.get("isVideoPaused") is True:
        return 0.0, "isVideoPaused is True; expected False while modal open"
    return 1.0, "Opened a post modal with video playing"


def _validate_openvideopause(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    if final_state.get("activePostId") != "2":
        return 0.0, f"activePostId={final_state.get('activePostId')} expected '2'"
    if final_state.get("isVideoPaused") is not True:
        return 0.0, "Video is not paused after opening post 2"
    return 1.0, "Opened post 2 video and paused it"


def _validate_searchandfollowall(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    current_user, error = _get_current_user(final_state)
    if not current_user:
        return 0.0, error
    ok, err = _check_exact_list(
        current_user.get("following"),
        ("1", "2", "3", "4", "5"),
        "currentUser.following",
    )
    if not ok:
        return 0.0, err

    for uid in ("1", "2", "3", "4", "5"):
        user, error = _find_user(final_state, uid)
        if not user:
            return 0.0, error
        followers = user.get("followers")
        if not isinstance(followers, list) or "0" not in followers:
            return 0.0, f"User {uid} followers={followers} expected to include '0'"

    if final_state.get("page") != "explore":
        return 0.0, f"page is {final_state.get('page')} expected 'explore'"

    return 1.0, "Followed all users 1-5 and returned to explore"


def _validate_search_and_like(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    post, error = _find_post(final_state, "1")
    if not post:
        return 0.0, error
    if post.get("likes") != 1:
        return 0.0, f"Post 1 likes={post.get('likes')} expected 1"

    user1, error = _find_user(final_state, "1")
    if not user1:
        return 0.0, error
    if user1.get("likeCount") != 1:
        return 0.0, f"User 1 likeCount={user1.get('likeCount')} expected 1"

    return 1.0, "Searched and liked post 1"


def _validate_search_input(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    if final_state.get("searchQuery") != "hello":
        return 0.0, f"searchQuery={final_state.get('searchQuery')} expected 'hello'"
    return 1.0, "Updated search input to 'hello'"


def _validate_searchuserandlikeall(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    target_posts = ("2", "7", "12", "17")
    for pid in target_posts:
        post, error = _find_post(final_state, pid)
        if not post:
            return 0.0, error
        if post.get("likes") != 1:
            return 0.0, f"Post {pid} likes={post.get('likes')} expected 1"

    user2, error = _find_user(final_state, "2")
    if not user2:
        return 0.0, error
    if user2.get("likeCount") != 4:
        return 0.0, f"User 2 likeCount={user2.get('likeCount')} expected 4"

    current_user, error = _get_current_user(final_state)
    if not current_user:
        return 0.0, error
    ok, err = _check_exact_list(current_user.get("likedPosts"), target_posts, "currentUser.likedPosts")
    if not ok:
        return 0.0, err

    return 1.0, "Liked all posts from user 2"


def _validate_unfollowuser(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    current_user, error = _get_current_user(final_state)
    if not current_user:
        return 0.0, error
    following = current_user.get("following")
    if not isinstance(following, list) or len(following) != 0:
        return 0.0, f"currentUser.following={following} expected empty list"

    user1, error = _find_user(final_state, "1")
    if not user1:
        return 0.0, error
    followers = user1.get("followers")
    if not isinstance(followers, list) or len(followers) != 0:
        return 0.0, f"User 1 followers={followers} expected empty list"

    if final_state.get("page") != "profile" or final_state.get("profileUserId") != "1":
        return 0.0, (f"page={final_state.get('page')} profileUserId={final_state.get('profileUserId')} expected profile/1")

    return 1.0, "Successfully unfollowed user 1 while viewing their profile"


def _validate_unlikepost(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    post, error = _find_post(final_state, "10")
    if not post:
        return 0.0, error
    if post.get("likes") != 0:
        return 0.0, f"Post 10 likes={post.get('likes')} expected 0"

    current_user, error = _get_current_user(final_state)
    if not current_user:
        return 0.0, error
    liked_posts = current_user.get("likedPosts")
    if not isinstance(liked_posts, list) or len(liked_posts) != 0:
        return 0.0, f"currentUser.likedPosts={liked_posts} expected empty list"

    return 1.0, "Unliked post 10 and cleared likedPosts"


def _validate_watchfullvideo(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    if final_state.get("activePostId") != "2":
        return 0.0, f"activePostId={final_state.get('activePostId')} expected '2'"
    if final_state.get("isVideoPaused") is not True:
        return 0.0, "Video is not paused at completion"
    if final_state.get("isVideoEnded") is not True:
        return 0.0, "isVideoEnded is not True after watching video"
    return 1.0, "Watched post 2 video through completion"


def _validate_bookmarkalbumcommentreply(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    page_requirements = (
        ("page", "album"),
        ("previousPage", "profile"),
        ("profileView", "bookmarks"),
        ("albumOwnerId", "0"),
    )
    for field, expected in page_requirements:
        value = final_state.get(field)
        if value != expected:
            return 0.0, f"{field}={value} expected '{expected}'"
    if not final_state.get("activeAlbumId"):
        return 0.0, "activeAlbumId is missing"
    if final_state.get("activePostId") != "6":
        return 0.0, f"activePostId={final_state.get('activePostId')} expected '6'"

    post, error = _find_post(final_state, "6")
    if not post:
        return 0.0, error
    if post.get("bookmarks") != 1:
        return 0.0, f"Post 6 bookmarks={post.get('bookmarks')} expected 1"

    comments = post.get("comments")
    if not isinstance(comments, list) or len(comments) < 2:
        return 0.0, "Post 6 does not contain the expected comments"
    nice_comments = [
        comment
        for comment in comments
        if isinstance(comment.get("content"), str) and comment["content"].strip().lower() == "nice"
    ]
    if len(nice_comments) != 2:
        return 0.0, f"Post 6 has {len(nice_comments)} comments with content 'nice', expected 2"
    ids = {comment.get("id") for comment in nice_comments if comment.get("id")}
    has_reply_link = any(comment.get("parentId") in ids for comment in nice_comments)
    if not has_reply_link:
        return 0.0, "Nice comments on post 6 are not linked via parentId as expected"

    current_user, error = _get_current_user(final_state)
    if not current_user:
        return 0.0, error
    bookmarks = current_user.get("bookmarks")
    if not isinstance(bookmarks, list) or "6" not in bookmarks:
        return 0.0, f"currentUser.bookmarks={bookmarks} expected to include '6'"

    album, error = _find_album_by_name(current_user, "cats")
    if not album:
        return 0.0, error
    post_ids = album.get("postIds")
    if not isinstance(post_ids, list) or "6" not in post_ids:
        return 0.0, f"Album 'cats' postIds={post_ids} expected to include '6'"

    return 1.0, "Post 6 bookmarked to new 'cats' album with comment chain and correct navigation state"


def _validate_commentinteractionseries(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    def _comment_contains(post: Dict[str, Any], *, expected_parent: str, expected_content: str) -> bool:
        target = expected_content.strip().lower()
        for comment in post.get("comments", []):
            if (
                isinstance(comment.get("content"), str)
                and comment["content"].strip().lower() == target
                and comment.get("parentId") == expected_parent
            ):
                return True
        return False

    post1, error = _find_post(final_state, "1")
    if not post1:
        return 0.0, error
    for cid in ("c1", "c1-1"):
        comment, error = _find_comment(post1, cid)
        if not comment:
            return 0.0, error
        liked = comment.get("likedBy")
        if not isinstance(liked, list) or "0" not in liked:
            return 0.0, f"Comment {cid} likedBy={liked} expected to include '0'"
    if not _comment_contains(post1, expected_parent="c1-1", expected_content="nice"):
        return 0.0, "Post 1 missing reply 'nice' to comment c1-1"

    post2, error = _find_post(final_state, "2")
    if not post2:
        return 0.0, error
    comment, error = _find_comment(post2, "c2")
    if not comment:
        return 0.0, error
    liked = comment.get("likedBy")
    if not isinstance(liked, list) or "0" not in liked:
        return 0.0, f"Comment c2 likedBy={liked} expected to include '0'"
    if not _comment_contains(post2, expected_parent="c2", expected_content="nice2"):
        return 0.0, "Post 2 missing reply 'nice2' to comment c2"

    post3, error = _find_post(final_state, "3")
    if not post3:
        return 0.0, error
    comment, error = _find_comment(post3, "c3")
    if not comment:
        return 0.0, error
    liked = comment.get("likedBy")
    if not isinstance(liked, list) or "0" not in liked:
        return 0.0, f"Comment c3 likedBy={liked} expected to include '0'"
    if not _comment_contains(post3, expected_parent="c3", expected_content="nice3"):
        return 0.0, "Post 3 missing reply 'nice3' to comment c3"

    if final_state.get("page") != "explore":
        return 0.0, f"page={final_state.get('page')} expected 'explore' after completing replies"

    return 1.0, "Liked and replied to the required comment series across posts 1-3"


def _validate_darkmodenotiflike(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    if final_state.get("themeMode") != "dark":
        return 0.0, f"themeMode={final_state.get('themeMode')} expected 'dark'"
    if final_state.get("page") != "explore" or final_state.get("previousPage") != "notifications":
        return 0.0, (
            f"page={final_state.get('page')} previousPage={final_state.get('previousPage')} expected explore/notifications"
        )
    post, error = _find_post(final_state, "1")
    if not post:
        return 0.0, error
    comment, error = _find_comment(post, "c1")
    if not comment:
        return 0.0, error
    liked = comment.get("likedBy")
    if not isinstance(liked, list) or "0" not in liked:
        return 0.0, f"Comment c1 likedBy={liked} expected to include '0'"
    return 1.0, "Enabled dark mode, handled notification, and liked the mention"


def _validate_findmention(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    if final_state.get("page") != "notifications" or final_state.get("previousPage") != "explore":
        return 0.0, (
            f"page={final_state.get('page')} previousPage={final_state.get('previousPage')} expected notifications/explore"
        )
    if final_state.get("activePostId") != "1":
        return 0.0, f"activePostId={final_state.get('activePostId')} expected '1'"
    if final_state.get("highlightCommentId") != "c1":
        return 0.0, f"highlightCommentId={final_state.get('highlightCommentId')} expected 'c1'"
    return 1.0, "Navigated to notifications and opened the mention thread"


def _validate_follownewfollower(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    current_user, error = _get_current_user(final_state)
    if not current_user:
        return 0.0, error
    following = current_user.get("following")
    if not isinstance(following, list) or "15" not in following:
        return 0.0, f"currentUser.following={following} expected to include '15'"

    new_user, error = _find_user(final_state, "15")
    if not new_user:
        return 0.0, error
    followers = new_user.get("followers")
    if not isinstance(followers, list) or "0" not in followers:
        return 0.0, f"User 15 followers={followers} expected to include '0'"

    if final_state.get("page") != "notifications" or final_state.get("previousPage") != "explore":
        return 0.0, (
            f"page={final_state.get('page')} previousPage={final_state.get('previousPage')} expected notifications/explore"
        )
    return 1.0, "Followed the new follower from notifications"


def _validate_replychain(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    post, error = _find_post(final_state, "1")
    if not post:
        return 0.0, error
    comments = post.get("comments")
    if not isinstance(comments, list):
        return 0.0, "Post 1 comments array missing"
    if len(comments) != 3:
        return 0.0, f"Post 1 has {len(comments)} comments, expected 3 after reply"
    has_nested_reply = any(
        isinstance(comment.get("content"), str)
        and comment["content"].strip().lower() == "nice"
        and comment.get("parentId") == "c1-1"
        for comment in comments
    )
    if not has_nested_reply:
        return 0.0, "Failed to find reply with content 'nice' pointing to comment c1-1"
    return 1.0, "Submitted nested reply to comment c1-1"


def _validate_searchownprofilereply(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    if final_state.get("page") != "profile" or final_state.get("previousPage") != "search":
        return 0.0, (f"page={final_state.get('page')} previousPage={final_state.get('previousPage')} expected profile/search")
    if final_state.get("profileUserId") != "0":
        return 0.0, f"profileUserId={final_state.get('profileUserId')} expected '0'"
    if final_state.get("activePostId") != "2":
        return 0.0, f"activePostId={final_state.get('activePostId')} expected '2'"

    post, error = _find_post(final_state, "2")
    if not post:
        return 0.0, error
    comments = post.get("comments")
    if not isinstance(comments, list) or len(comments) < 2:
        return 0.0, "Post 2 is missing expected reply comments"
    has_reply = any(
        isinstance(comment.get("content"), str)
        and comment["content"].strip().lower() == "nice"
        and comment.get("parentId") == "c2"
        for comment in comments
    )
    if not has_reply:
        return 0.0, "Post 2 is missing reply 'nice' to comment c2"
    return 1.0, "Replied to comment on own profile after search"


def _validate_albumview(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    for field, expected in (("page", "profile"), ("previousPage", "explore"), ("profileView", "bookmarks")):
        value = final_state.get(field)
        if value != expected:
            return 0.0, f"{field}={value} expected '{expected}'"
    return 1.0, "Profile bookmarks view is visible from album grid"


def _validate_backpage(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    if final_state.get("page") != "profile":
        return 0.0, f"page={final_state.get('page')} expected 'profile'"
    if final_state.get("previousPage") != "album":
        return 0.0, f"previousPage={final_state.get('previousPage')} expected 'album'"
    if final_state.get("profileUserId") != "0":
        return 0.0, f"profileUserId={final_state.get('profileUserId')} expected '0'"
    return 1.0, "Returned to profile from album view using back navigation"


def _validate_bookmarkalbum(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    for pid in ("1", "2"):
        post, error = _find_post(final_state, pid)
        if not post:
            return 0.0, error
        if post.get("bookmarks") != 1:
            return 0.0, f"Post {pid} bookmarks={post.get('bookmarks')} expected 1"

    current_user, error = _get_current_user(final_state)
    if not current_user:
        return 0.0, error
    ok, err = _check_exact_list(current_user.get("bookmarks"), ("1", "2"), "currentUser.bookmarks")
    if not ok:
        return 0.0, err

    album, error = _find_album_by_name(current_user, "yoo")
    if not album:
        return 0.0, error
    ok, err = _check_exact_list(album.get("postIds"), ("2",), "Album 'yoo' postIds")
    if not ok:
        return 0.0, err

    return 1.0, "Bookmarked posts 1 and 2 and added post 2 to album 'yoo'"


def _validate_bookmarkandlike(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    required_fields = (
        ("page", "profile"),
        ("previousPage", "explore"),
        ("profileView", "bookmarks"),
        ("profileUserId", "0"),
    )
    for field, expected in required_fields:
        value = final_state.get(field)
        if value != expected:
            return 0.0, f"{field}={value} expected '{expected}'"

    if final_state.get("activePostId") != "1":
        return 0.0, f"activePostId={final_state.get('activePostId')} expected '1'"

    post, error = _find_post(final_state, "1")
    if not post:
        return 0.0, error
    if post.get("likes") != 1 or post.get("bookmarks") != 1:
        return 0.0, (
            f"Post 1 likes/bookmarks mismatch. likes={post.get('likes')} bookmarks={post.get('bookmarks')} expected 1/1"
        )

    current_user, error = _get_current_user(final_state)
    if not current_user:
        return 0.0, error
    ok, err = _check_exact_list(current_user.get("bookmarks"), ("1",), "currentUser.bookmarks")
    if not ok:
        return 0.0, err
    ok, err = _check_exact_list(current_user.get("likedPosts"), ("1",), "currentUser.likedPosts")
    if not ok:
        return 0.0, err

    return 1.0, "Bookmarked and liked post 1 while viewing profile bookmarks"


def _validate_bookmarksview(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    if final_state.get("page") != "profile":
        return 0.0, f"page={final_state.get('page')} expected 'profile'"
    if final_state.get("previousPage") != "explore":
        return 0.0, f"previousPage={final_state.get('previousPage')} expected 'explore'"
    if final_state.get("profileView") != "bookmarks":
        return 0.0, f"profileView={final_state.get('profileView')} expected 'bookmarks'"
    if final_state.get("profileUserId") != "0":
        return 0.0, f"profileUserId={final_state.get('profileUserId')} expected '0'"
    return 1.0, "Viewing current user's bookmarks"


def _validate_createalbumadd(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    for pid in ("1", "2"):
        post, error = _find_post(final_state, pid)
        if not post:
            return 0.0, error
        if post.get("bookmarks") != 1:
            return 0.0, f"Post {pid} bookmarks={post.get('bookmarks')} expected 1"

    current_user, error = _get_current_user(final_state)
    if not current_user:
        return 0.0, error
    ok, err = _check_exact_list(current_user.get("bookmarks"), ("1", "2"), "currentUser.bookmarks")
    if not ok:
        return 0.0, err

    album, error = _find_album_by_name(current_user, "yo")
    if not album:
        return 0.0, error
    post_ids = album.get("postIds")
    if not isinstance(post_ids, list) or sorted(post_ids) != ["1", "2"]:
        return 0.0, f"Album 'yo' postIds={post_ids} expected ['1', '2']"

    return 1.0, "Created album 'yo' containing bookmarked posts 1 and 2"


def _validate_darkmode(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    if final_state.get("themeMode") != "dark":
        return 0.0, f"themeMode={final_state.get('themeMode')} expected 'dark'"
    return 1.0, "Theme set to dark mode"


def _validate_darkmodefilter(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    if final_state.get("themeMode") != "dark":
        return 0.0, f"themeMode={final_state.get('themeMode')} expected 'dark'"
    if final_state.get("feedFilter") != "校园日常":
        return 0.0, f"feedFilter={final_state.get('feedFilter')} expected '校园日常'"
    return 1.0, "Dark mode enabled and feed filter set to 校园日常"


def _validate_darkmodelike(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    field_expectations = (("page", "explore"), ("previousPage", "explore"), ("themeMode", "dark"))
    for field, expected in field_expectations:
        value = final_state.get(field)
        if value != expected:
            return 0.0, f"{field}={value} expected '{expected}'"

    post, error = _find_post(final_state, "1")
    if not post:
        return 0.0, error
    if post.get("likes") != 1:
        return 0.0, f"Post 1 likes={post.get('likes')} expected 1"

    current_user, error = _get_current_user(final_state)
    if not current_user:
        return 0.0, error
    likes = current_user.get("likedPosts")
    if not isinstance(likes, list) or "1" not in likes:
        return 0.0, f"currentUser.likedPosts={likes} expected to include '1'"

    return 1.0, "Liked post 1 while dark mode remained enabled"


def _validate_darkmodesearchwatch(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    expected = (("page", "search"), ("previousPage", "explore"), ("searchQuery", "oo"), ("themeMode", "dark"))
    for field, value in expected:
        current = final_state.get(field)
        if current != value:
            return 0.0, f"{field}={current} expected '{value}'"
    if final_state.get("activePostId") != "1":
        return 0.0, f"activePostId={final_state.get('activePostId')} expected '1'"
    return 1.0, "Searched for 'oo', switched to dark mode, and watched post 1"


def _validate_filtercommentprofiledark(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    expectations = (
        ("page", "profile"),
        ("previousPage", "explore"),
        ("feedFilter", "萌宠日常"),
        ("profileUserId", "0"),
        ("themeMode", "dark"),
    )
    for field, expected in expectations:
        value = final_state.get(field)
        if value != expected:
            return 0.0, f"{field}={value} expected '{expected}'"

    post, error = _find_post(final_state, "2")
    if not post:
        return 0.0, error
    ok, err = _validate_single_comment(post, "nice")
    if not ok:
        return 0.0, err

    return 1.0, "Filtered feed, commented on post 2, returned to profile, and enabled dark mode"


def _validate_lightmode(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    if final_state.get("themeMode") != "light":
        return 0.0, f"themeMode={final_state.get('themeMode')} expected 'light'"
    return 1.0, "Theme set to light mode"


def _validate_likesearchfollowdark(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    expectations = (
        ("page", "search"),
        ("previousPage", "explore"),
        ("searchQuery", "妹妹宝"),
        ("themeMode", "dark"),
        ("searchFilter", "用户"),
    )
    for field, expected in expectations:
        value = final_state.get(field)
        if value != expected:
            return 0.0, f"{field}={value} expected '{expected}'"

    post, error = _find_post(final_state, "1")
    if not post:
        return 0.0, error
    if post.get("likes") != 1:
        return 0.0, f"Post 1 likes={post.get('likes')} expected 1"

    user2, error = _find_user(final_state, "2")
    if not user2:
        return 0.0, error
    followers = user2.get("followers")
    if not isinstance(followers, list) or followers != ["0"]:
        return 0.0, f"User 2 followers={followers} expected ['0']"

    current_user, error = _get_current_user(final_state)
    if not current_user:
        return 0.0, error
    following = current_user.get("following")
    if not isinstance(following, list) or "2" not in following:
        return 0.0, f"currentUser.following={following} expected to include '2'"

    return 1.0, "Liked a post, searched for user 妹妹宝, followed them, and enabled dark mode"


def _validate_likesview(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    if final_state.get("page") != "profile":
        return 0.0, f"page={final_state.get('page')} expected 'profile'"
    if final_state.get("previousPage") != "explore":
        return 0.0, f"previousPage={final_state.get('previousPage')} expected 'explore'"
    if final_state.get("profileView") != "likes":
        return 0.0, f"profileView={final_state.get('profileView')} expected 'likes'"
    if final_state.get("profileUserId") != "0":
        return 0.0, f"profileUserId={final_state.get('profileUserId')} expected '0'"
    return 1.0, "Viewing current user's liked posts"


def _validate_openalbumwatchvideo(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    if final_state.get("page") != "album":
        return 0.0, f"page={final_state.get('page')} expected 'album'"
    if final_state.get("previousPage") != "profile":
        return 0.0, f"previousPage={final_state.get('previousPage')} expected 'profile'"
    if not final_state.get("activeAlbumId"):
        return 0.0, "activeAlbumId missing or empty"
    if final_state.get("activePostId") != "1":
        return 0.0, f"activePostId={final_state.get('activePostId')} expected '1'"
    if final_state.get("isVideoPaused") is not True:
        return 0.0, "Video is not paused after watching album video"
    if final_state.get("isVideoEnded") is not True:
        return 0.0, "isVideoEnded is not True after watching album video"
    return 1.0, "Opened an album, played post 1, and watched it to completion"


def _validate_openanalbum(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    if final_state.get("page") != "album":
        return 0.0, f"page={final_state.get('page')} expected 'album'"
    if final_state.get("previousPage") != "profile":
        return 0.0, f"previousPage={final_state.get('previousPage')} expected 'profile'"
    if not final_state.get("activeAlbumId"):
        return 0.0, "activeAlbumId missing or empty"
    return 1.0, "Opened an album from the profile grid"


def _validate_removebookmarksinalbum(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    current_user, error = _get_current_user(final_state)
    if not current_user:
        return 0.0, error

    bookmarks = current_user.get("bookmarks")
    if not isinstance(bookmarks, list) or bookmarks:
        return 0.0, f"currentUser.bookmarks={bookmarks} expected empty list"

    album, error = _find_album_by_name(current_user, "yo")
    if not album:
        return 0.0, error
    post_ids = album.get("postIds")
    if not isinstance(post_ids, list) or post_ids:
        return 0.0, f"Album 'yo' postIds={post_ids} expected empty list"

    return 1.0, "Removed all bookmarked posts from album 'yo'"


def _validate_searchlikeunbookmark(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    expectations = (
        ("page", "profile"),
        ("previousPage", "search"),
        ("profileView", "bookmarks"),
        ("profileUserId", "0"),
    )
    for field, expected in expectations:
        value = final_state.get(field)
        if value != expected:
            return 0.0, f"{field}={value} expected '{expected}'"

    if final_state.get("activePostId") is not None:
        return 0.0, f"activePostId={final_state.get('activePostId')} expected None"

    post, error = _find_post(final_state, "1")
    if not post:
        return 0.0, error
    if post.get("likes") != 1:
        return 0.0, f"Post 1 likes={post.get('likes')} expected 1"
    if post.get("bookmarks") not in (0, None):
        return 0.0, f"Post 1 bookmarks={post.get('bookmarks')} expected 0"

    current_user, error = _get_current_user(final_state)
    if not current_user:
        return 0.0, error
    bookmarks = current_user.get("bookmarks")
    if not isinstance(bookmarks, list) or bookmarks:
        return 0.0, f"currentUser.bookmarks={bookmarks} expected empty list"
    likes = current_user.get("likedPosts")
    if not isinstance(likes, list) or "1" not in likes:
        return 0.0, f"currentUser.likedPosts={likes} expected to include '1'"

    return 1.0, "Searched, liked post 1, and then removed it from bookmarks"


def _validate_setfilter(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    if final_state.get("feedFilter") != "OOTD":
        return 0.0, f"feedFilter={final_state.get('feedFilter')} expected 'OOTD'"
    return 1.0, "Feed filter set to OOTD"


def _validate_systemtheme(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    if final_state.get("themeMode") != "system":
        return 0.0, f"themeMode={final_state.get('themeMode')} expected 'system'"
    return 1.0, "Theme set to follow system setting"


def _validate_unlikecurrentuserlikes(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    current_user, error = _get_current_user(final_state)
    if not current_user:
        return 0.0, error
    liked = current_user.get("likedPosts")
    if not isinstance(liked, list) or liked:
        return 0.0, f"currentUser.likedPosts={liked} expected empty list"

    post, error = _find_post(final_state, "1")
    if not post:
        return 0.0, error
    if post.get("likes") not in (0, None):
        return 0.0, f"Post 1 likes={post.get('likes')} expected 0"

    return 1.0, "Cleared current user's liked posts by unliking post 1"


# Registry of all Xiaohongshu reward functions
REWARD_FUNCTIONS_XIAOHONGSHU = {
    "_validate_albumview": _validate_albumview,
    "_validate_backpage": _validate_backpage,
    "_validate_bookmarkalbum": _validate_bookmarkalbum,
    "_validate_bookmarkalbumcommentreply": _validate_bookmarkalbumcommentreply,
    "_validate_bookmarkandlike": _validate_bookmarkandlike,
    "_validate_bookmarkpost": _validate_bookmarkpost,
    "_validate_bookmarksview": _validate_bookmarksview,
    "_validate_commentinteractionseries": _validate_commentinteractionseries,
    "_validate_commentontwoseparateposts": _validate_commentontwoseparateposts,
    "_validate_commentonvideo": _validate_commentonvideo,
    "_validate_comprehensiveuserinteraction": _validate_comprehensiveuserinteraction,
    "_validate_createalbumadd": _validate_createalbumadd,
    "_validate_crossuserengagement": _validate_crossuserengagement,
    "_validate_darkmodenotiflike": _validate_darkmodenotiflike,
    "_validate_darkmode": _validate_darkmode,
    "_validate_darkmodefilter": _validate_darkmodefilter,
    "_validate_darkmodelike": _validate_darkmodelike,
    "_validate_darkmodesearchwatch": _validate_darkmodesearchwatch,
    "_validate_findmention": _validate_findmention,
    "_validate_filtercommentprofiledark": _validate_filtercommentprofiledark,
    "_validate_follownavigatehome": _validate_follownavigatehome,
    "_validate_follownewfollower": _validate_follownewfollower,
    "_validate_followuser": _validate_followuser,
    "_validate_lightmode": _validate_lightmode,
    "_validate_like3sequential": _validate_like3sequential,
    "_validate_likeandbookmark": _validate_likeandbookmark,
    "_validate_likepost": _validate_likepost,
    "_validate_likesearchfollowdark": _validate_likesearchfollowdark,
    "_validate_likesview": _validate_likesview,
    "_validate_navigateownprofile": _validate_navigateownprofile,
    "_validate_openalbumwatchvideo": _validate_openalbumwatchvideo,
    "_validate_openanalbum": _validate_openanalbum,
    "_validate_openpostmodal": _validate_openpostmodal,
    "_validate_openvideopause": _validate_openvideopause,
    "_validate_replychain": _validate_replychain,
    "_validate_searchandfollowall": _validate_searchandfollowall,
    "_validate_search_and_like": _validate_search_and_like,
    "_validate_search_input": _validate_search_input,
    "_validate_searchownprofilereply": _validate_searchownprofilereply,
    "_validate_searchlikeunbookmark": _validate_searchlikeunbookmark,
    "_validate_searchuserandlikeall": _validate_searchuserandlikeall,
    "_validate_setfilter": _validate_setfilter,
    "_validate_systemtheme": _validate_systemtheme,
    "_validate_unfollowuser": _validate_unfollowuser,
    "_validate_unlikecurrentuserlikes": _validate_unlikecurrentuserlikes,
    "_validate_unlikepost": _validate_unlikepost,
    "_validate_watchfullvideo": _validate_watchfullvideo,
    "_validate_removebookmarksinalbum": _validate_removebookmarksinalbum,
}
