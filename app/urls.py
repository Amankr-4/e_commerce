from django.urls import path
from app import views
# for image taking
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .forms import LoginForm , password_change , password_reset_form ,password_confirm_form
urlpatterns = [
    # path('', views.home),
    
    path('',views.productview.as_view(),name= 'home'),
    path('product-detail/<int:pk>', views.productdetails.as_view(), name='product-detail'),
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.show_cart, name='show-cart'),
    path('pluscart/',views.plus_cart ),
    path('minuscart/',views.minus_cart ),
    path('removecart/',views.remove_cart ),
    
    
    path('buy/', views.buy_now, name='buy-now'),
    path('accounts/profile/', views.ProfileView.as_view(), name='profile'),
    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),
    #with help of old password                                                                                                                      #success_url mltb ye h ki agar password successfully change ho jaye to '/passwordchangedone/' yaha redirect kae do 
    path('passwordchange/', auth_views.PasswordChangeView.as_view(template_name='app/passwordchange.html',form_class=password_change,success_url ='/passwordchangedone/'), name='passwordchange'),
    path('passwordchangedone/',auth_views.PasswordChangeDoneView.as_view(template_name='app/passwordchangedone.html'),name='passwordchangedone'),
    # password pura bhul chuke h humme reset karna h by email                                                                                                                               # niche charo me name yahi likhna padega warna erroe aayega since hum saare chiz inbuild use kar rhe h isliye
    path('passwordreset/',auth_views.PasswordResetView.as_view(template_name = 'app/password_reset.html',form_class=password_reset_form),name = 'password_reset'),
    path('passwordreset/done/',auth_views.PasswordResetDoneView.as_view(template_name = 'app/password_reset_done.html'),name = 'password_reset_done'),                        
    path('password-reset-confirm/<uidb64>/<token>',auth_views.PasswordResetConfirmView.as_view(template_name = 'app/password_reset_confirm.html',form_class =password_confirm_form ),name = 'password_reset_confirm'),
    path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(template_name = 'app/password_reset_complete.html'),name = 'password_reset_complete'),
    
    path('mobile/', views.mobile, name='mobile'),
    path('mobile/<slug:data>', views.mobile, name='mobiledata'), #since data string type ka h n isliye slug likhe h hmm
    path('accounts/login/', auth_views.LoginView.as_view(template_name='app/login.html',authentication_form=LoginForm), name='login'), 
    #login ke liye view me kucch likhne ke liye koi jarurat nhi h yaha direct ho gya
    
   
    path('logout/',views.user_logout,name='logout'),
    path('registration/', views.customerRegistration.as_view(), name='customerregistration'),
    path('checkout/', views.checkout, name='checkout'),
    path('paymentdone/',views.payment_done,name = 'payment_done')
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT) # for image uploading and to show it on frontend dynamically
