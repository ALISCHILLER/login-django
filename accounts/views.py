import logging
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import APIException
from .Serializer import SignupSerializer
from .models import MyUser
import logging


# تنظیمات لاگ‌گذاری
logger = logging.getLogger(__name__)


# ویو برای ثبت‌نام کاربر
class SignupView(APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            return Response({'message': 'کاربر با موفقیت ایجاد شد.'}, status=status.HTTP_201_CREATED)

        # بازگشت خطاها به صورت جزیی
        logger.error(f"Signup failed: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ویو برای ورود کاربر
class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(request, email=email, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })

        logger.warning(f"Failed login attempt for email: {email}")
        return Response({'error': 'ایمیل یا رمز عبور اشتباه است'}, status=status.HTTP_401_UNAUTHORIZED)


# ویو برای بررسی توکن
from rest_framework.permissions import IsAuthenticated



logger = logging.getLogger(__name__)

class VerifyTokenView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            # بررسی وضعیت حساب کاربر
            if not request.user.is_active:
                logger.warning(f"User {request.user.email} attempted to use an inactive account.")
                raise APIException("حساب کاربری شما غیر فعال است.")

            # ارسال پاسخ
            return Response({
                'status': 'success',
                'message': 'توکن معتبر است',
                'data': {
                    'user': {
                        'id': request.user.id,
                        'email': request.user.email,
                    }
                }
            }, status=status.HTTP_200_OK)

        except APIException as e:
            # مدیریت خطاهای مربوط به اعتبارسنجی و حساب‌های غیرفعال
            logger.error(f"Error during token verification: {str(e)}")
            return Response({'status': 'error', 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            # مدیریت خطاهای عمومی و لاگ‌گذاری آن‌ها
            logger.critical(f"Unexpected error: {str(e)}", exc_info=True)  # exc_info=True برای نمایش اطلاعات خطا در لاگ
            return Response({
                'status': 'error',
                'message': 'خطای غیرمنتظره رخ داده است.',
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


