import unittest
from gitgrind import main
import pygit2
import logging

class TestGitGrind(unittest.TestCase):
    def check_need(self, need, found):
        commit = [x for x in found['normal'] if x.id == need][0]
        logging.info("check %s", str(commit))
        epoch = str(commit.id)
        logging.info("Epoch: %s", epoch)
        self.assertTrue(epoch == need) 
        return commit

    def test_epoch(self):
        repo = pygit2.Repository('.')
        grind = main.GitGrind(repo)
        found = grind.grind("author == 'kurt godwin'", "logic")
        logging.info("Found: %s", found)
        self.check_need("9342134002bca2bef1ec8e9d63a6ec5690558d62", found)

    def test_initial_message(self):
        repo = pygit2.Repository('.')
        grind = main.GitGrind(repo,logger=logging)
        found = grind.grind("message == 'workflow updates'", "logic")
        commit = self.check_need("939dd6bd244d6e37b397b40b36af2b1a7faac5db", found)
        logging.info("Message: %s",commit.message)
        self.assertTrue('workflow updates' in commit.message.lower())
        
    def test_repo(self):
        repo = pygit2.Repository('.')
        logging.info("References: %s", list(repo.references))
