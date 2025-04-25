from flask import Blueprint, abort, render_template

subs_bp = Blueprint("subscriptions", __name__)


@subs_bp.route("/store/subscriptions")
def subscription_listings():
    from models import get_sample_subscription_data

    # Get all sample subscription plans
    subscriptions = [get_sample_subscription_data(i) for i in range(1, 4)]
    return render_template("subscription_listings.html", subscriptions=subscriptions)


@subs_bp.route("/store/subscriptions/<int:plan_id>")
@subs_bp.route("/subscription/<int:plan_id>")
def subscription_details(plan_id):
    # Updated subscription data with AI tools, DM tools, and game creation focus
    all_subscriptions = [
        {
            "id": 1,
            "tier": "Basic",
            "name": "Basic Plan",
            "short_description": "Essential tools for beginners",
            "description": "Start your journey with essential storytelling and game creation tools.",
            "price": 10,
            "billing_cycle": "month",
            "features": [
                "LoreTeller AI (Limited)",
                "Basic character creation",
                "5 campaign slots",
                "Standard support",
            ],
            "feature_descriptions": {
                "LoreTeller AI (Limited)": "Access to basic AI story generation with up to 2,000 tokens per day",
                "Basic character creation": "Create and customize up to 10 characters with basic attributes",
                "5 campaign slots": "Manage up to 5 active campaigns simultaneously",
                "Standard support": "Email support with 48-hour response time",
            },
            "key_features": [
                "Essential storytelling tools",
                "Basic AI assistance",
                "Core game mechanics",
            ],
            "is_popular": False,
            "reviews": [
                {
                    "customer_name": "John D.",
                    "rating": 4,
                    "content": "Great starter option for my small campaigns. Easy to use and covers the basics I need.",
                }
            ],
            "faqs": [
                {
                    "question": "Can I upgrade to a higher plan later?",
                    "answer": "Yes, you can upgrade to a higher plan at any time with prorated billing.",
                }
            ],
        },
        {
            "id": 2,
            "tier": "Premium",
            "name": "Premium Plan",
            "short_description": "Advanced tools for serious storytellers",
            "description": "Enhance your storytelling with advanced AI features and DM tools.",
            "price": 25,
            "billing_cycle": "month",
            "features": [
                "LoreTeller AI (Advanced)",
                "DM Tools Suite",
                "15 campaign slots",
                "Custom NPC generator",
                "Priority support",
            ],
            "feature_descriptions": {
                "LoreTeller AI (Advanced)": "Enhanced AI story generation with up to 10,000 tokens per day and more creative options",
                "DM Tools Suite": "Complete set of tools for campaign management, including initiative tracker and encounter builder",
                "15 campaign slots": "Manage up to 15 active campaigns simultaneously",
                "Custom NPC generator": "Create unique NPCs with detailed backgrounds and personalities",
                "Priority support": "Priority email support with 24-hour response time",
            },
            "key_features": [
                "Advanced AI storytelling",
                "Complete DM toolset",
                "Enhanced campaign management",
            ],
            "is_popular": True,
            "reviews": [
                {
                    "customer_name": "Lisa R.",
                    "rating": 5,
                    "content": "The Premium Plan has been a game-changer for my campaigns. The DM tools save me hours of prep time.",
                }
            ],
            "faqs": [
                {
                    "question": "What are DM Tools?",
                    "answer": "DM Tools include encounter builders, initiative trackers, loot generators, and other utilities to make running your games smoother.",
                }
            ],
        },
        {
            "id": 3,
            "tier": "Ultimate",
            "name": "Ultimate Plan",
            "short_description": "Professional-grade world building",
            "description": "The complete suite for professional game masters and world builders.",
            "price": 50,
            "billing_cycle": "month",
            "features": [
                "LoreTeller AI (Unlimited)",
                "Complete DM Tools Suite",
                "Unlimited campaign slots",
                "LoreMaker Game Engine",
                "Basic API access",
                "24/7 priority support",
            ],
            "feature_descriptions": {
                "LoreTeller AI (Unlimited)": "Unlimited AI story generation with priority processing and all creative options",
                "Complete DM Tools Suite": "Full access to all DM tools with advanced customization options",
                "Unlimited campaign slots": "No limits on the number of campaigns you can create and manage",
                "LoreMaker Game Engine": "Create and publish your own games using our intuitive game engine",
                "Basic API access": "Access our API to build custom integrations (5,000 calls/month)",
                "24/7 priority support": "Round-the-clock support via email, chat, and phone",
            },
            "key_features": [
                "Unlimited AI capabilities",
                "Game creation engine",
                "Professional-grade tools",
                "Developer API access",
            ],
            "is_popular": False,
            "reviews": [
                {
                    "customer_name": "Creative Studios",
                    "rating": 5,
                    "content": "The Ultimate Plan provides everything we need for our professional game development team. Worth every penny.",
                }
            ],
            "faqs": [
                {
                    "question": "What can I do with the LoreMaker Game Engine?",
                    "answer": "The LoreMaker Game Engine allows you to create, test, and publish your own games with simple drag-and-drop interfaces and custom scripting options.",
                }
            ],
        },
        {
            "id": 4,
            "tier": "Enterprise",
            "name": "Enterprise Plan",
            "short_description": "Custom solutions for organizations",
            "description": "Tailored solutions for educational institutions, publishers, and game studios.",
            "price": None,
            "contact_us": True,
            "billing_cycle": "custom",
            "features": [
                "Custom AI model training",
                "White-labeled platform",
                "Unlimited everything",
                "Full API access",
                "Enterprise SLA",
                "Dedicated account manager",
                "Custom integrations",
            ],
            "feature_descriptions": {
                "Custom AI model training": "Train custom AI models on your own content and lore",
                "White-labeled platform": "Fully customizable and brandable platform for your organization",
                "Unlimited everything": "No limitations on any platform features or usage",
                "Full API access": "Unlimited API access with dedicated endpoints for your organization",
                "Enterprise SLA": "Custom Service Level Agreement with guaranteed uptime and performance",
                "Dedicated account manager": "Personal account manager for your organization",
                "Custom integrations": "Custom development for specific needs and integrations",
            },
            "key_features": [
                "Custom AI solutions",
                "White-labeled platform",
                "Dedicated support team",
                "Custom development",
            ],
            "is_popular": False,
            "reviews": [
                {
                    "customer_name": "Global Gaming Academy",
                    "rating": 5,
                    "content": "The Enterprise Plan allowed us to create a custom platform for our students with our own branding and curriculum integration.",
                }
            ],
            "faqs": [
                {
                    "question": "How do I get started with an Enterprise plan?",
                    "answer": "Contact our sales team to schedule a consultation. We'll work with you to understand your needs and create a custom solution.",
                }
            ],
        },
    ]

    # Find the subscription with the matching ID
    subscription = next(
        (sub for sub in all_subscriptions if sub["id"] == plan_id), None
    )

    if not subscription:
        abort(404)

    # Get all features across all plans for comparison
    all_features = set()
    for sub in all_subscriptions:
        all_features.update(sub["features"])
    all_features = sorted(list(all_features))

    return render_template(
        "subscription_details.html",
        subscription=subscription,
        comparison_plans=all_subscriptions,
        all_features=all_features,
    )


@subs_bp.route("/subscribe/<int:subscription_id>")
def subscribe(subscription_id):
    # Placeholder for subscription purchase process
    # This would typically connect to a payment processor
    return f"Subscribe to plan {subscription_id} - Payment form would go here"


@subs_bp.route("/subscriptions")
def subscriptions():
    # Simplified subscription data
    subscriptions = [
        {
            "id": 1,
            "tier": "Basic",
            "name": "Starter Plan",
            "description": "Perfect for individuals and small projects.",
            "price": 9.99,
            "billing_cycle": "month",
            "features": [
                "Limited access to resources",
                "Basic reporting",
                "Email support",
                "Single user",
            ],
            "is_popular": False,
        },
        {
            "id": 2,
            "tier": "Pro",
            "name": "Professional Plan",
            "description": "Ideal for growing businesses and teams.",
            "price": 29.99,
            "billing_cycle": "month",
            "features": [
                "Full access to resources",
                "Advanced reporting",
                "Priority email support",
                "Up to 10 users",
            ],
            "is_popular": True,
            "savings": 20,
        },
        {
            "id": 3,
            "tier": "Enterprise",
            "name": "Enterprise Plan",
            "description": "Complete solution for large organizations.",
            "price": 99.99,
            "billing_cycle": "month",
            "features": [
                "Unlimited access to resources",
                "Real-time reporting and analytics",
                "24/7 dedicated support",
                "Unlimited users",
            ],
            "is_popular": False,
            "savings": 15,
        },
    ]
    return render_template("subscriptions.html", subscriptions=subscriptions)
