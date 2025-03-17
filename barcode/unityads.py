# SDK: UnityAds: android.gradle_dependencies = com.unity3d.ads:unity-ads:4.13.2

from jnius import autoclass, PythonJavaClass, java_method

# Load Java Classes
UnityAds = autoclass("com.unity3d.ads.UnityAds")
UnityAdsShowOptions = autoclass("com.unity3d.ads.UnityAdsShowOptions")
PythonActivity = autoclass("org.kivy.android.PythonActivity")


# ✅ Custom UnityAdsLoadListener
class UnityAdsLoadListener(PythonJavaClass):
    __javainterfaces__ = ['com.unity3d.ads.IUnityAdsLoadListener']
    __javacontext__ = 'app'

    def __init__(self,load_state_callback):
        super().__init__()
        self.load_state_ = load_state_callback  # Store the callback function

    @java_method('(Ljava/lang/String;)V')
    def onUnityAdsAdLoaded(self, placementId):
        self.load_state_(state=True)
        print(f"✅ Ad {placementId} loaded successfully!")

    @java_method('(Ljava/lang/String;Lcom/unity3d/ads/UnityAds$UnityAdsLoadError;Ljava/lang/String;)V')
    def onUnityAdsFailedToLoad(self, placementId, error, message):
        self.load_state_(state=False)
        print(f"❌ Failed to load ad {placementId}: {error}, {message}")


# ✅ Custom UnityAdsShowListener (With Callback)
class UnityAdsShowListener(PythonJavaClass):
    __javainterfaces__ = ['com.unity3d.ads.IUnityAdsShowListener']
    __javacontext__ = 'app'

    def __init__(self,_ad_mngr ,reward_callback):
        super().__init__()
        self._ad_manager = _ad_mngr
        self.reward_callback = reward_callback  # Store the callback function

    @java_method('(Ljava/lang/String;Lcom/unity3d/ads/UnityAds$UnityAdsShowCompletionState;)V')
    def onUnityAdsShowComplete(self, placementId, state):
        print(f"✅ Ad {placementId} {state} completed!")
        # Call the reward function
        if self.reward_callback:
            self.reward_callback()
        # Reload ad
        self._ad_manager.load_ad()

    @java_method('(Ljava/lang/String;)V')
    def onUnityAdsShowStart(self, placementId):
        print(f"🎬 Ad {placementId} started.")

    @java_method('(Ljava/lang/String;Lcom/unity3d/ads/UnityAds$UnityAdsShowError;Ljava/lang/String;)V')
    def onUnityAdsShowFailure(self, placementId, error, message):
        print(f"❌ Failed to show ad {placementId}: {error}, {message}")

    @java_method('(Ljava/lang/String;)V')
    def onUnityAdsShowClick(self, placementId):
        print(f"👆 Ad {placementId} clicked.")


# ✅ UnityAdManager Class 
class UnityAdManager:
    def __init__(self, game_id="5734872", ad_unit_id="Rewarded_Android", test_mode=True):
        self.game_id = game_id
        self.ad_unit_id = ad_unit_id if ad_unit_id == "Rewarded_Android" else "Rewarded_Android"
        self.test_mode = test_mode
        self.activity = PythonActivity.mActivity
        self._manager =  None
        self.reward_callback = None  # Default callback (None)
        self.load_state_callback = None  # Default callback (None)

        UnityAds.initialize(self.activity, self.game_id, self.test_mode)

    def set_ad_manager(self, manager):
        self._manager = manager

    def set_reward_callback(self, callback):
        self.reward_callback = callback  # Store the callback function

    def set_load_state_callback(self, callback):
        self.load_state_callback = callback

    def load_ad(self):
        if self.load_state_callback:
            self.load_listener = UnityAdsLoadListener(self.load_state_callback)
            UnityAds.load(self.ad_unit_id, self.load_listener)
            print("🔄 Loading the ad...")
        else:
            print("⚠️ Load state callback not set!")

    def show_ad(self):
        if self.reward_callback:
            self.show_listener = UnityAdsShowListener(self._manager,self.reward_callback)
            try:
              UnityAds.show(self.activity, self.ad_unit_id, UnityAdsShowOptions(), self.show_listener)
            except Exception as e:
              print("Ads not loaded yet ", e)
        else:
            print("⚠️ Reward callback not set!")



"""
# ✅ Kivy App Code
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout

KV = '''
BoxLayout:
    orientation: 'vertical'
    Label:
        id: coin_label
        text: "Coins: " + str(app.coin)
    Button:
        text: 'Show Rewarded Ad'
        on_release: app.show_rewarded_ad()
'''


class MyApp(App):
    coin = 0  # Initialize coin count

    def build(self):
        
        self.ad_manager = UnityAdManager(test_mode=False)  # Initialize UnityAdManager
        
        self.ad_manager.set_ad_manager(self.ad_manager)  # Set the ad manager
        self.ad_manager.set_reward_callback(self.reward_user)  # Set reward callback
        self.ad_manager.set_load_state_callback(self.on_ad_loaded)

        self.ad_manager.load_ad()


        return Builder.load_string(KV)

    def show_rewarded_ad(self):
        self.ad_manager.show_ad()

    # def on_stop(self):
        # UnityAds.destroy
    
    def on_ad_loaded(self, state):
        print("Ad loaded state: ", state)

    def reward_user(self):
        print("🎉 Rewarding user with 10 coins!")
        self.coin += 10
        self.update_coin_display()

    def update_coin_display(self):
        self.root.ids.coin_label.text = f"Coins: {self.coin}"


_app = MyApp()
_app.run()
"
"""