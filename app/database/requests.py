import random

from app.database.models import async_session
from app.database.models import User, Photo, Video, Photo_approve, Video_approve
from sqlalchemy import select, func

async def check_user(user_id: int) -> None:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == user_id))

        if not user:
            session.add(User(tg_id=user_id, user_status="user", user_photo=1, user_video=1))
            await session.commit()
            user = await session.scalar(select(User).where(User.tg_id == user_id))

        return user.user_status

async def get_content(user_id):
    contend_data = None
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == user_id))
        user_photo = user.user_photo
        user_video = user.user_video

        result_photo = await session.execute(select(func.max(Photo.id)))
        max_photo = result_photo.scalar()

        result_video = await session.execute(select(func.max(Video.id)))
        max_video = result_video.scalar()
        if (user_photo <= max_photo) and (user_video <= max_video):
            random_choose = random.randint(0,1)
            if random_choose == 0:
                photo = await session.scalar(select(Photo).where(Photo.id == user_photo))
                user.user_photo = user_photo+1
                contend_data = [photo.tg_id, "photo"]
            else:
                video = await session.scalar(select(Video).where(Video.id == user_video))
                user.user_video = user_video+1
                contend_data = [video.tg_id, "video"]
        elif user_photo <= max_photo:
            photo = await session.scalar(select(Photo).where(Photo.id == user_photo))
            user.user_photo = user_photo+1
            contend_data = [photo.tg_id, "photo"]
        elif user_video <= max_video:
            video = await session.scalar(select(Video).where(Video.id == user_video))
            user.user_video = user_video+1
            contend_data = [video.tg_id, "video"]
        else:
            contend_data = ["No content", 'No content']
            
        await session.commit()
    
    return contend_data
    
async def reset_user_counter(user_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == user_id))
        user.user_photo = 1
        user.user_video = 1
        await session.commit()


async def save_photo(tg_id):
    async with async_session() as session:
        photo = await session.scalar(select(Photo).where(Photo.tg_id == tg_id))
        photo_approve = await session.scalar(select(Photo_approve).where(Photo_approve.tg_id == tg_id))
        if photo or photo_approve:
            await delete_photo(tg_id)
        else:
            new_photo = Photo_approve(tg_id=tg_id)
            session.add(new_photo)
            await session.commit()

async def save_video(tg_id):
    async with async_session() as session:
        video = await session.scalar(select(Video).where(Video.tg_id == tg_id))
        video_approve = await session.scalar(select(Video_approve).where(Video_approve.tg_id == tg_id))
        if video or video_approve:
            await delete_video(tg_id)
        else:
            new_photo = Video_approve(tg_id=tg_id)
            session.add(new_photo)
            await session.commit()

async def get_content_to_approve():
    contend_data = None
    async with async_session() as session:
        result_photo = await session.execute(select(func.max(Photo_approve.id)))
        max_photo = result_photo.scalar()

        result_video = await session.execute(select(func.max(Video_approve.id)))
        max_video = result_video.scalar()

        if max_photo and max_video:
            random_choose = random.randint(0,1)
            if random_choose == 0:
                photo = await session.scalar(select(Photo_approve).where(Photo_approve.id == max_photo))
                contend_data = [photo.tg_id, "photo"]
            else:
                video = await session.scalar(select(Video_approve).where(Video_approve.id == max_video))
                contend_data = [video.tg_id, "video"]
        elif max_photo:
            photo = await session.scalar(select(Photo_approve).where(Photo_approve.id == max_photo))
            contend_data = [photo.tg_id, "photo"]
        elif max_video:
            video = await session.scalar(select(Video_approve).where(Video_approve.id == max_video))
            contend_data = [video.tg_id, "video"]
        else:
            contend_data = ["No content", 'No content']

    return contend_data

async def accept_photo(tg_id):
    async with async_session() as session:
        photo = await session.scalar(select(Photo).where(Photo.tg_id == tg_id))
        if photo:
            pass
        else:
            new_photo = Photo(tg_id=tg_id)
            session.add(new_photo)
            await session.commit()
    await delete_photo(tg_id)


async def accept_video(tg_id):
    async with async_session() as session:
        photo = await session.scalar(select(Video).where(Video.tg_id == tg_id))
        if photo:
            pass
        else:
            new_photo = Video(tg_id=tg_id)
            session.add(new_photo)
            await session.commit()
    await delete_video(tg_id)


async def delete_photo(tg_id):
    async with async_session() as session:
        photo = await session.scalar(select(Photo_approve).where(Photo_approve.tg_id == tg_id))
        await session.delete(photo)
        await session.commit()
    

async def delete_video(tg_id):
    async with async_session() as session:
        video = await session.scalar(select(Video_approve).where(Video_approve.tg_id == tg_id))
        await session.delete(video)
        await session.commit()