import json
from glob import glob
import models
from models import FantiaClub, POST_API, traceback
from session_arg import session_arg, fanclub_urls  # type: ignore

def download_remaining_posts(fanclub, downloader):
    """Get post ids and downloaded for fanclub and filters on downloader from
    folder lookup.
    """
    post_ids = downloader.fetch_fanclub_posts(fanclub)
    response = downloader.session.get(POST_API.format(post_ids[0]))
    response.raise_for_status()
    post_json = json.loads(response.text)["post"]
    creator_name = post_json["fanclub"]["creator_name"]
    downloaded_ids = glob('./{}/*'.format(creator_name))
    downloaded_ids = [id.split('/')[-1] for id in downloaded_ids]
    for post_id in post_ids:
        if post_id not in downloaded_ids:
            try:
                downloader.download_post(post_id)
            except KeyboardInterrupt:
                raise
            except:
                if downloader.continue_on_error:
                    downloader.output("Encountered an error downloading post. Skipping...\n")
                    traceback.print_exc()
                    continue
                else:
                    raise


if __name__ == '__main__':
    for fanclub_url in fanclub_urls:
        print('fanclub_url: {}'.format(fanclub_url))
        url_match = models.FANTIA_URL_RE.match(fanclub_url)
        url_groups = url_match.groups()
        downloader = models.FantiaDownloader(session_arg=session_arg, quiet=False)
        fanclub = models.FantiaClub(url_groups[1])
        download_remaining_posts(fanclub, downloader)
