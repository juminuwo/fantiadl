import json
import os
from glob import glob

from bs4 import BeautifulSoup

import models
from models import *
from cmdl_values import fanclub_urls, session_arg  # type: ignore
from models import POST_API, FantiaClub, traceback

# Use the project directory as output path
output_path = os.path.dirname(os.path.abspath(__file__))


def download_remaining_posts(output_path, fanclub, downloader):
    """Get post ids and downloaded for fanclub and filters on downloader from
    folder lookup.
    """
    post_ids = downloader.fetch_fanclub_posts(fanclub)
    post_html_response = downloader.session.get(POST_URL.format(post_ids[0]))
    post_html_response.raise_for_status()
    post_html = BeautifulSoup(post_html_response.text, "html.parser")
    csrf_token = post_html.select_one("meta[name=\"csrf-token\"]")["content"]

    response = downloader.session.get(POST_API.format(post_ids[0]), headers={
        "X-CSRF-Token": csrf_token,
        "X-Requested-With": "XMLHttpRequest"
    })
    response.raise_for_status()
    post_json = json.loads(response.text)["post"]

    creator_name = post_json["fanclub"]["creator_name"]
    downloaded_ids = glob('{}/{}/*'.format(output_path, creator_name))
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
        downloader = models.FantiaDownloader(session_arg=session_arg, quiet=False, directory=output_path)
        fanclub = models.FantiaClub(url_groups[1])
        download_remaining_posts(output_path, fanclub, downloader)
