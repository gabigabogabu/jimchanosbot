import praw
import logging
from time import sleep

reactions = {
    'should i sell': 'yes',
}


def get_logger(name, level):
    new_log = logging.getLogger(name)
    log_format = '[%(asctime)s] [%(levelname)s] - %(message)s'

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(logging.Formatter(log_format))
    new_log.addHandler(stream_handler)

    fileHandler = logging.FileHandler('grootbot.new_log')
    fileHandler.setFormatter(logging.Formatter(log_format))
    new_log.addHandler(fileHandler)

    new_log.setLevel(level=level)
    return new_log


def configure_logging():
    global log
    get_logger("praw", logging.INFO)
    get_logger("prawcore", logging.INFO)
    log = get_logger("chanosbot", logging.DEBUG)


def config_reddit():
    new_reddit = praw.Reddit('bot')
    log.info('logged in')
    return new_reddit


def handle_comment(comment):
    log.debug(str(comment.author) + ':\t' + comment.body)

    # don't comment on own comments
    if comment.author == reddit.user.me():
        log.info('own comment found: %s', comment.id)
        return

    for r in reactions.keys():
        if r in comment.body.lower():
            log.info('"{}" comment found'.format(r))
            # comment.reply(reactions[r])


if __name__ == "__main__":
    configure_logging()
    reddit = config_reddit()

    sleepUntilNextTry = 0
    while True:
        try:
            for c in reddit.subreddit('teslainvestorsclub').stream.comments():
                handle_comment(c)
                sleepUntilNextTry = 0
        except Exception as e:
            log.critical('well shit: ' + str(e))
            sleepUntilNextTry += .1
            log.critical('sleeping %ss', sleepUntilNextTry)
            sleep(sleepUntilNextTry)
            continue