# flake8: noqa: E501

false = False
null = None

undo = {
    "@context": "https://www.w3.org/ns/activitystreams",
    "id": "https://23.social/users/andreasofthings#follows/58530/undo",
    "type": "Undo",
    "actor": "https://23.social/users/andreasofthings",
    "object": {
        "id": "https://23.social/e6630b4e-9401-4c26-9091-e3570cea344e",
        "type": "Follow",
        "actor": "https://23.social/users/andreasofthings",
        "object": "https://pramari.de/@andreas",
    },
}


follow = {
    "@context": "https://www.w3.org/ns/activitystreams",
    "id": "https://pramari.de/113eb421-8273-4b29-b418-9d1aeffe26e2",
    "type": "Follow",
    "actor": "https://pramari.de/@andreas",
    "object": "https://pramari.de/@andreas",
}

mention = {
    "@context": [
        "https://www.w3.org/ns/activitystreams",
        {
            "ostatus": "http://ostatus.org#",
            "atomUri": "ostatus:atomUri",
            "inReplyToAtomUri": "ostatus:inReplyToAtomUri",
            "conversation": "ostatus:conversation",
            "sensitive": "as:sensitive",
            "toot": "http://joinmastodon.org/ns#",
            "votersCount": "toot:votersCount",
        },
    ],
    "id": "https://23.social/users/andreasofthings/statuses/112621194858481951/activity",
    "type": "Create",
    "actor": "https://23.social/users/andreasofthings",
    "published": "2024-06-15T14:50:56Z",
    "to": ["https://www.w3.org/ns/activitystreams#Public"],
    "cc": [
        "https://23.social/users/andreasofthings/followers",
        "https://pramari.de/@andreas",
    ],
    "object": {
        "id": "https://23.social/users/andreasofthings/statuses/112621194858481951",
        "type": "Note",
        "summary": null,
        "inReplyTo": null,
        "published": "2024-06-15T14:50:56Z",
        "url": "https://23.social/@andreasofthings/112621194858481951",
        "attributedTo": "https://23.social/users/andreasofthings",
        "to": ["https://www.w3.org/ns/activitystreams#Public"],
        "cc": [
            "https://23.social/users/andreasofthings/followers",
            "https://pramari.de/@andreas",
        ],
        "sensitive": false,
        "atomUri": "https://23.social/users/andreasofthings/statuses/112621194858481951",
        "inReplyToAtomUri": null,
        "conversation": "tag:23.social,2024-06-15:objectId=3873286:objectType=Conversation",
        "content": '\u003cp\u003e\u003cspan class="h-card" translate="no"\u003e\u003ca href="https://pramari.de/@andreas" class="u-url mention"\u003e@\u003cspan\u003eandreas\u003c/span\u003e\u003c/a\u003e\u003c/span\u003e Test!\u003c/p\u003e',
        "contentMap": {
            "en": '\u003cp\u003e\u003cspan class="h-card" translate="no"\u003e\u003ca href="https://pramari.de/@andreas" class="u-url mention"\u003e@\u003cspan\u003eandreas\u003c/span\u003e\u003c/a\u003e\u003c/span\u003e Test!\u003c/p\u003e'
        },
        "attachment": [],
        "tag": [
            {
                "type": "Mention",
                "href": "https://pramari.de/@andreas",
                "name": "@andreas@pramari.de",
            }
        ],
        "replies": {
            "id": "https://23.social/users/andreasofthings/statuses/112621194858481951/replies",
            "type": "Collection",
            "first": {
                "type": "CollectionPage",
                "next": "https://23.social/users/andreasofthings/statuses/112621194858481951/replies?only_other_accounts=true\u0026page=true",
                "partOf": "https://23.social/users/andreasofthings/statuses/112621194858481951/replies",
                "items": [],
            },
        },
    },
    "signature": {
        "type": "RsaSignature2017",
        "creator": "https://23.social/users/andreasofthings#main-key",
        "created": "2024-06-15T14:50:56Z",
        "signatureValue": "ntW2W8BA5rQntHA6wBy+meR7W/XR8nlv74MKoBWKySK2tCbTWtnSvb3PHiIlmhpnabrBj/IUg3dPJwTRwe9a/raBsBSvLfPnLheo/9Ra25AGgEtBAimClmwYGZpO9CDrvPQJPisjkMBKHnkSDW7+TvnvUEVXfleU1ImA8stly3XvhPiuapfxFlygRBltNddUxzUJ+CjNAUb0hMrS/P9aH2z6jwa+o3X1YOhBoqXkg+krTKbECLLumlVhB5SfL6NpCXQVTA5qNn/W4ej2W5oNbzmsDWUscvathuk4hF0livfhm8gEKwFNTaZx15miVmGqueXwQVwDu/Gh6i4S5b844w==",
    },
}

"""
https://www.w3.org/TR/activitystreams-vocabulary/
"""

w3c_activity = {
    "accept": [
        {
            "@context": "https://www.w3.org/ns/activitystreams",
            "summary": "Sally accepted an invitation to a party",
            "@type": "Accept",
            "actor": {"type": "Person", "name": "Sally"},
            "object": {
                "type": "Invite",
                "actor": "http://john.example.org",
                "object": {"type": "Event", "name": "Going-Away Party for Jim"},
            },
        },
        {
            "@context": "https://www.w3.org/ns/activitystreams",
            "summary": "Sally accepted Joe into the club",
            "type": "Accept",
            "actor": {"type": "Person", "name": "Sally"},
            "object": {"type": "Person", "name": "Joe"},
            "target": {"type": "Group", "name": "The Club"},
        },
        {
            "context": "https://www.w3.org/ns/activitystreams",
            "@id": "https://www.w3.org/ns/activitystreams",
            "summary": "Sally accepted Joe into the club",
            "type": "Accept",
            "actor": {"type": "Person", "name": "Sally"},
            "object": {"type": "Person", "name": "Joe"},
            "target": {"type": "Group", "name": "The Club"},
        },
    ],
    "tentative_accept": [
        {
            "@context": "https://www.w3.org/ns/activitystreams",
            "summary": "Sally tentatively accepted an invitation to a party",
            "type": "TentativeAccept",
            "actor": {"type": "Person", "name": "Sally"},
            "object": {
                "type": "Invite",
                "actor": "http://john.example.org",
                "object": {"type": "Event", "name": "Going-Away Party for Jim"},
            },
        }
    ],
    "add": [
        {
            "@context": "https://www.w3.org/ns/activitystreams",
            "summary": "Sally added an object",
            "type": "Add",
            "actor": {"type": "Person", "name": "Sally"},
            "object": "http://example.org/abc",
        },
        {
            "@context": "https://www.w3.org/ns/activitystreams",
            "summary": "Sally added a picture of her cat to her cat picture collection",
            "type": "Add",
            "actor": {"type": "Person", "name": "Sally"},
            "object": {
                "type": "Image",
                "name": "A picture of my cat",
                "url": "http://example.org/img/cat.png",
            },
            "origin": {"type": "Collection", "name": "Camera Roll"},
            "target": {"type": "Collection", "name": "My Cat Pictures"},
        },
    ],
    "arrive": [
        {
            "@context": "https://www.w3.org/ns/activitystreams",
            "summary": "Sally arrived at work",
            "type": "Arrive",
            "actor": {"type": "Person", "name": "Sally"},
            "location": {"type": "Place", "name": "Work"},
            "origin": {"type": "Place", "name": "Home"},
        }
    ],
    "create": [
        {
            "@context": "https://www.w3.org/ns/activitystreams",
            "summary": "Sally created a note",
            "type": "Create",
            "actor": {"type": "Person", "name": "Sally"},
            "object": {
                "type": "Note",
                "name": "A Simple Note",
                "content": "This is a simple note",
            },
        }
    ],
    "delete": [
        {
            "@context": "https://www.w3.org/ns/activitystreams",
            "summary": "Sally deleted a note",
            "type": "Delete",
            "actor": {"type": "Person", "name": "Sally"},
            "object": "http://example.org/notes/1",
            "origin": {"type": "Collection", "name": "Sally's Notes"},
        }
    ],
    "follow": [
        {
            "@context": "https://www.w3.org/ns/activitystreams",
            "summary": "Sally followed John",
            "type": "Follow",
            "actor": {"type": "Person", "name": "Sally"},
            "object": {"type": "Person", "name": "John"},
        }
    ],
    "ignore": [
        {
            "@context": "https://www.w3.org/ns/activitystreams",
            "summary": "Sally ignored a note",
            "type": "Ignore",
            "actor": {"type": "Person", "name": "Sally"},
            "object": "http://example.org/notes/1",
        }
    ],
    "join": [
        {
            "@context": "https://www.w3.org/ns/activitystreams",
            "summary": "Sally joined a group",
            "type": "Join",
            "actor": {"type": "Person", "name": "Sally"},
            "object": {"type": "Group", "name": "A Simple Group"},
        }
    ],
    "leave": [
        {
            "@context": "https://www.w3.org/ns/activitystreams",
            "summary": "Sally left work",
            "type": "Leave",
            "actor": {"type": "Person", "name": "Sally"},
            "object": {"type": "Place", "name": "Work"},
        },
        {
            "@context": "https://www.w3.org/ns/activitystreams",
            "summary": "Sally left a group",
            "type": "Leave",
            "actor": {"type": "Person", "name": "Sally"},
            "object": {"type": "Group", "name": "A Simple Group"},
        },
    ],
    "like": [
        {
            "@context": "https://www.w3.org/ns/activitystreams",
            "summary": "Sally liked a note",
            "type": "Like",
            "actor": {"type": "Person", "name": "Sally"},
            "object": "http://example.org/notes/1",
        }
    ],
    "offer": [
        {
            "@context": "https://www.w3.org/ns/activitystreams",
            "summary": "Sally offered 50% off to Lewis",
            "type": "Offer",
            "actor": {"type": "Person", "name": "Sally"},
            "object": {
                "type": "http://www.types.example/ProductOffer",
                "name": "50% Off!",
            },
            "target": {"type": "Person", "name": "Lewis"},
        }
    ],
    "invite": [
        {
            "@context": "https://www.w3.org/ns/activitystreams",
            "summary": "Sally invited John and Lisa to a party",
            "type": "Invite",
            "actor": {"type": "Person", "name": "Sally"},
            "object": {"type": "Event", "name": "A Party"},
            "target": [
                {"type": "Person", "name": "John"},
                {"type": "Person", "name": "Lisa"},
            ],
        }
    ],
    "reject": [
        {
            "@context": "https://www.w3.org/ns/activitystreams",
            "summary": "Sally rejected an invitation to a party",
            "type": "Reject",
            "actor": {"type": "Person", "name": "Sally"},
            "object": {
                "type": "Invite",
                "actor": "http://john.example.org",
                "object": {"type": "Event", "name": "Going-Away Party for Jim"},
            },
        }
    ],
    "tentativereject": [
        {
            "@context": "https://www.w3.org/ns/activitystreams",
            "summary": "Sally tentatively rejected an invitation to a party",
            "type": "TentativeReject",
            "actor": {"type": "Person", "name": "Sally"},
            "object": {
                "type": "Invite",
                "actor": "http://john.example.org",
                "object": {"type": "Event", "name": "Going-Away Party for Jim"},
            },
        }
    ],
    "remove": [
        {
            "@context": "https://www.w3.org/ns/activitystreams",
            "summary": "Sally removed a note from her notes folder",
            "type": "Remove",
            "actor": {"type": "Person", "name": "Sally"},
            "object": "http://example.org/notes/1",
            "target": {"type": "Collection", "name": "Notes Folder"},
        },
        {
            "@context": "https://www.w3.org/ns/activitystreams",
            "summary": "The moderator removed Sally from a group",
            "type": "Remove",
            "actor": {"type": "http://example.org/Role", "name": "The Moderator"},
            "object": {"type": "Person", "name": "Sally"},
            "origin": {"type": "Group", "name": "A Simple Group"},
        },
    ],
    "undo": [
        {
            "@context": "https://www.w3.org/ns/activitystreams",
            "summary": "Sally retracted her offer to John",
            "type": "Undo",
            "actor": "http://sally.example.org",
            "object": {
                "type": "Offer",
                "actor": "http://sally.example.org",
                "object": "http://example.org/posts/1",
                "target": "http://john.example.org",
            },
        }
    ],
    "update": [
        {
            "@context": "https://www.w3.org/ns/activitystreams",
            "summary": "Sally updated her note",
            "type": "Update",
            "actor": {"type": "Person", "name": "Sally"},
            "object": "http://example.org/notes/1",
        }
    ],
    "view": [
        {
            "@context": "https://www.w3.org/ns/activitystreams",
            "summary": "Sally read an article",
            "type": "View",
            "actor": {"type": "Person", "name": "Sally"},
            "object": {
                "type": "Article",
                "name": "What You Should Know About Activity Streams",
            },
        }
    ],
    "listen": [
        {
            "@context": "https://www.w3.org/ns/activitystreams",
            "summary": "Sally listened to a piece of music",
            "type": "Listen",
            "actor": {"type": "Person", "name": "Sally"},
            "object": "http://example.org/music.mp3",
        }
    ],
    "read": [
        {
            "@context": "https://www.w3.org/ns/activitystreams",
            "summary": "Sally read a blog post",
            "type": "Read",
            "actor": {"type": "Person", "name": "Sally"},
            "object": "http://example.org/posts/1",
        }
    ],
    "move": [
        {
            "@context": "https://www.w3.org/ns/activitystreams",
            "summary": "Sally moved a post from List A to List B",
            "type": "Move",
            "actor": {"type": "Person", "name": "Sally"},
            "object": "http://example.org/posts/1",
            "target": {"type": "Collection", "name": "List B"},
            "origin": {"type": "Collection", "name": "List A"},
        }
    ],
    "travel": [
        {
            "@context": "https://www.w3.org/ns/activitystreams",
            "summary": "Sally went home from work",
            "type": "Travel",
            "actor": {"type": "Person", "name": "Sally"},
            "target": {"type": "Place", "name": "Home"},
            "origin": {"type": "Place", "name": "Work"},
        }
    ],
    "Announce": [
        {
            "@context": "https://www.w3.org/ns/activitystreams",
            "summary": "Sally announced that she had arrived at work",
            "type": "Announce",
            "actor": {
                "type": "Person",
                "id": "http://sally.example.org",
                "name": "Sally",
            },
            "object": {
                "type": "Arrive",
                "actor": "http://sally.example.org",
                "location": {"type": "Place", "name": "Work"},
            },
        }
    ],
    "block": [
        {
            "@context": "https://www.w3.org/ns/activitystreams",
            "summary": "Sally blocked Joe",
            "type": "Block",
            "actor": "http://sally.example.org",
            "object": "http://joe.example.org",
        }
    ],
    "flag": [
        {
            "@context": "https://www.w3.org/ns/activitystreams",
            "summary": "Sally flagged an inappropriate note",
            "type": "Flag",
            "actor": "http://sally.example.org",
            "object": {"type": "Note", "content": "An inappropriate note"},
        }
    ],
    "dislike": [
        {
            "@context": "https://www.w3.org/ns/activitystreams",
            "summary": "Sally disliked a post",
            "type": "Dislike",
            "actor": "http://sally.example.org",
            "object": "http://example.org/posts/1",
        }
    ],
    "question": [
        {
            "@context": "https://www.w3.org/ns/activitystreams",
            "type": "Question",
            "name": "What is the answer?",
            "oneOf": [
                {"type": "Note", "name": "Option A"},
                {"type": "Note", "name": "Option B"},
            ],
        },
        {
            "@context": "https://www.w3.org/ns/activitystreams",
            "type": "Question",
            "name": "What is the answer?",
            "closed": "2016-05-10T00:00:00Z",
        },
    ],
}
